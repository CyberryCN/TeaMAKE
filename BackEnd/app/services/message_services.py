from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy import func

from app.models.message import Conversation, Message, Application
from app.models.recruitment import Recruitment
from app.models.team import Team, TeamMember
from app.models.enums import ApplicationStatus, RecruitStatus


def send_application(db: Session, recruitment_id: int, applicant_id: int, receiver_id: int) -> Application:
    """
    用户A向用户B发送组队申请
    """
    application = Application(
        recruitment_id=recruitment_id,
        applicant_id=applicant_id,
        receiver_id=receiver_id,
        status=ApplicationStatus.WAITING.value,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_unread_application_count(db: Session, user_id: int) -> int:
    """
    获取用户B收到的未读申请数量（状态为WAITING）
    用于消息界面红点显示
    """
    return db.query(func.count(Application.id)).filter(
        Application.receiver_id == user_id,
        Application.status == ApplicationStatus.WAITING.value
    ).scalar()


def get_received_applications(db: Session, user_id: int, status: Optional[str] = None) -> List[Application]:
    """
    用户C在私聊界面查看收到的申请
    可选按状态筛选（waiting/accept/reject）
    """
    query = db.query(Application).filter(Application.receiver_id == user_id)

    if status:
        query = query.filter(Application.status == status)

    return query.order_by(Application.created_at.desc()).all()


def get_sent_applications(db: Session, user_id: int, status: Optional[str] = None) -> List[Application]:
    """
    用户查看自己发出的申请
    """
    query = db.query(Application).filter(Application.applicant_id == user_id)

    if status:
        query = query.filter(Application.status == status)

    return query.order_by(Application.created_at.desc()).all()


def get_all_user_applications(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[Application]:
    """
    用户D在个人主页查看所有相关申请（发起+接收）
    分页返回，默认最近50条
    """
    return db.query(Application).filter(
        or_(Application.applicant_id == user_id, Application.receiver_id == user_id)
    ).order_by(Application.created_at.desc()).offset(skip).limit(limit).all()


def respond_to_application(db: Session, application_id: int, responder_id: int, accept: bool) -> Optional[Application]:
    """
    用户B响应申请：接受或拒绝
    接受时自动创建/加入队伍，并增加人数
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.receiver_id == responder_id,  # 只有接收者可以响应
        Application.status == ApplicationStatus.WAITING.value  # 只能响应等待中的
    ).first()

    if not application:
        return None

    if accept:
        application.status = ApplicationStatus.ACCEPT.value

        # 获取招募信息
        recruitment = db.query(Recruitment).filter(
            Recruitment.id == application.recruitment_id
        ).first()

        if recruitment:
            # 检查是否已有队伍，没有则创建
            team = db.query(Team).filter(Team.recruitment_id == recruitment.id).first()
            if not team:
                # 创建队伍
                team = Team(
                    recruitment_id=recruitment.id,
                    name=f"{recruitment.title} 队伍",
                    description=recruitment.description,
                    competition_name=recruitment.competition_name,
                    competition_url=recruitment.competition_url,
                )
                db.add(team)
                db.flush()

                # 添加接收者（队长）
                leader = TeamMember(
                    team_id=team.id,
                    user_id=responder_id,
                    role="leader"
                )
                db.add(leader)

            # 添加申请者为队员
            existing_member = db.query(TeamMember).filter(
                TeamMember.team_id == team.id,
                TeamMember.user_id == application.applicant_id
            ).first()

            if not existing_member:
                member = TeamMember(
                    team_id=team.id,
                    user_id=application.applicant_id,
                    role="member"
                )
                db.add(member)

                # 招募当前人数 +1（新加入的成员）
                recruitment.current_number += 1

                db.flush()

                # 检查是否满员，满员则关闭招募
                if recruitment.current_number >= recruitment.required_number:
                    recruitment.status = RecruitStatus.COMPLETED.value
    else:
        application.status = ApplicationStatus.REJECT.value

    db.commit()
    db.refresh(application)

    return application