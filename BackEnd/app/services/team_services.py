from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.recruitment import Recruitment
from app.models.team import Team, TeamMember
from app.models.skill import Skill
from app.models.enums import RecruitStatus


def create_team_for_recruitment(db: Session, recruitment: Recruitment, creator_id: int) -> Team:
    """为招募创建队伍，创建者自动成为队长"""
    team = Team(
        recruitment_id=recruitment.id,
        name=f"{recruitment.title} 队伍",
        description=recruitment.description,
        competition_name=recruitment.competition_name,
        competition_url=recruitment.competition_url,
    )
    db.add(team)
    db.flush()

    # 创建者成为队长
    leader = TeamMember(
        team_id=team.id,
        user_id=creator_id,
        role="leader"
    )
    db.add(leader)

    db.commit()
    db.refresh(team)
    return team


def get_team_by_id(db: Session, team_id: int) -> Optional[Team]:
    """根据ID获取队伍"""
    return db.query(Team).filter(Team.id == team_id).first()


def get_team_by_recruitment(db: Session, recruitment_id: int) -> Optional[Team]:
    """根据招募ID获取队伍"""
    return db.query(Team).filter(Team.recruitment_id == recruitment_id).first()


def get_user_teams(db: Session, user_id: int) -> List[Team]:
    """获取用户加入的所有队伍"""
    team_ids = db.query(TeamMember.team_id).filter(TeamMember.user_id == user_id).all()
    team_ids = [t[0] for t in team_ids]
    if not team_ids:
        return []
    return db.query(Team).filter(Team.id.in_(team_ids)).all()


def get_team_members(db: Session, team_id: int) -> List[TeamMember]:
    """获取队伍所有成员"""
    return db.query(TeamMember).filter(TeamMember.team_id == team_id).all()


def add_team_member(db: Session, team_id: int, user_id: int, role: str = "member") -> Optional[TeamMember]:
    """添加队伍成员"""
    # 检查是否已是成员
    existing = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    if existing:
        return existing

    member = TeamMember(
        team_id=team_id,
        user_id=user_id,
        role=role
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def remove_team_member(db: Session, team_id: int, user_id: int) -> bool:
    """移除队伍成员"""
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    if not member:
        return False

    db.delete(member)
    db.commit()
    return True
