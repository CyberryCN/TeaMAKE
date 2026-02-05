from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.recruitment import Recruitment
from app.models.skill import Skill
from app.models.team import Team
from app.models.enums import RecruitStatus
from app.services import team_services as ts


def get_recruitment_by_id(db: Session, recruitment_id: int) -> Optional[Recruitment]:
    """根据ID获取招募"""
    return db.query(Recruitment).filter(Recruitment.id == recruitment_id).first()


def get_recruitments_by_user(db: Session, user_id: int, status: Optional[str] = None) -> List[Recruitment]:
    """获取用户的所有招募"""
    query = db.query(Recruitment).filter(Recruitment.creator_id == user_id)
    if status:
        query = query.filter(Recruitment.status == status)
    return query.order_by(Recruitment.created_at.desc()).all()


def get_recruitments(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    competition_name: Optional[str] = None
) -> tuple[List[Recruitment], int]:
    """获取招募列表（分页）"""
    query = db.query(Recruitment)

    if status:
        query = query.filter(Recruitment.status == status)
    if competition_name:
        query = query.filter(Recruitment.competition_name.contains(competition_name))

    # 只显示开放和已完成的状态
    query = query.filter(Recruitment.status.in_([RecruitStatus.OPEN.value, RecruitStatus.COMPLETED.value]))

    total = query.count()
    recruitments = query.order_by(Recruitment.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return recruitments, total


def post_recruitment(db: Session, user_id: int, title: str, description: str,
                     competition_name: str, competition_url: Optional[str],
                     required_number: int, deadline: datetime,
                     expected_start: datetime, expected_end: datetime,
                     required_skills: List[int] = None) -> Recruitment:
    """发布招募，同时创建队伍"""
    recruitment = Recruitment(
        creator_id=user_id,
        title=title,
        description=description,
        competition_name=competition_name,
        competition_url=competition_url,
        required_number=required_number,
        current_number=1,  # 创建者自己算一个人
        status=RecruitStatus.OPEN.value,
        deadline=deadline,
        expected_start=expected_start,
        expected_end=expected_end,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # 处理技能关联
    if required_skills:
        skills = db.query(Skill).filter(Skill.id.in_(required_skills)).all()
        recruitment.required_skills = skills

    db.add(recruitment)
    db.flush()  # 获取 recruitment.id

    # 创建队伍，创建者自动成为队长
    ts.create_team_for_recruitment(db, recruitment, user_id)

    db.commit()
    db.refresh(recruitment)
    return recruitment


def draft_recruitment(db: Session, user_id: int, title: Optional[str] = None,
                      description: Optional[str] = None, competition_name: Optional[str] = None,
                      competition_url: Optional[str] = None, required_number: int = 1,
                      deadline: Optional[datetime] = None,
                      expected_start: Optional[datetime] = None,
                      expected_end: Optional[datetime] = None,
                      required_skills: List[int] = None) -> Recruitment:
    """保存草稿"""
    recruitment = Recruitment(
        creator_id=user_id,
        title=title,
        description=description,
        competition_name=competition_name,
        competition_url=competition_url,
        required_number=required_number,
        current_number=0,
        status=RecruitStatus.DRAFT.value,
        deadline=deadline,
        expected_start=expected_start,
        expected_end=expected_end,
    )

    # 处理技能关联
    if required_skills:
        skills = db.query(Skill).filter(Skill.id.in_(required_skills)).all()
        recruitment.required_skills = skills

    db.add(recruitment)
    db.commit()
    db.refresh(recruitment)
    return recruitment


def update_recruitment(db: Session, recruitment_id: int, user_id: int,
                       **kwargs) -> Optional[Recruitment]:
    """更新招募（只能更新草稿或开放状态）"""
    recruitment = get_recruitment_by_id(db, recruitment_id)
    if not recruitment:
        return None

    if recruitment.creator_id != user_id:
        return None

    # 草稿可以更新所有字段，开放状态只能更新部分
    if recruitment.status == RecruitStatus.OPEN.value:
        allowed_fields = ['title', 'description', 'competition_name', 'competition_url',
                         'required_number', 'deadline', 'expected_start', 'expected_end']
    else:
        allowed_fields = []

    for key, value in kwargs.items():
        if key in allowed_fields or recruitment.status == RecruitStatus.DRAFT.value:
            setattr(recruitment, key, value)

    recruitment.updated_at = datetime.now(timezone.utc)

    # 处理技能更新
    if 'required_skills' in kwargs:
        skills = db.query(Skill).filter(Skill.id.in_(kwargs['required_skills'])).all()
        recruitment.required_skills = skills

    db.commit()
    db.refresh(recruitment)
    return recruitment


def publish_draft(db: Session, recruitment_id: int, user_id: int) -> Optional[Recruitment]:
    """发布草稿，同时创建队伍"""
    recruitment = get_recruitment_by_id(db, recruitment_id)
    if not recruitment:
        return None

    if recruitment.creator_id != user_id:
        return None

    if recruitment.status != RecruitStatus.DRAFT.value:
        return None

    # 检查必填字段
    if not all([recruitment.title, recruitment.description, recruitment.competition_name,
                recruitment.required_number, recruitment.deadline,
                recruitment.expected_start, recruitment.expected_end]):
        return None

    recruitment.status = RecruitStatus.OPEN.value
    recruitment.current_number = 1  # 创建者算一个人
    recruitment.updated_at = datetime.now(timezone.utc)

    # 创建队伍，创建者成为队长
    ts.create_team_for_recruitment(db, recruitment, user_id)

    db.commit()
    db.refresh(recruitment)
    return recruitment


def close_recruitment(db: Session, recruitment_id: int, user_id: int) -> Optional[Recruitment]:
    """关闭招募"""
    recruitment = get_recruitment_by_id(db, recruitment_id)
    if not recruitment:
        return None

    if recruitment.creator_id != user_id:
        return None

    if recruitment.status != RecruitStatus.OPEN.value:
        return None

    recruitment.status = RecruitStatus.CLOSED.value
    recruitment.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(recruitment)
    return recruitment


def delete_recruitment(db: Session, recruitment_id: int, user_id: int) -> bool:
    """删除招募（只能删除草稿）"""
    recruitment = get_recruitment_by_id(db, recruitment_id)
    if not recruitment:
        return False

    if recruitment.creator_id != user_id:
        return False

    if recruitment.status != RecruitStatus.DRAFT.value:
        return False

    db.delete(recruitment)
    db.commit()
    return True
