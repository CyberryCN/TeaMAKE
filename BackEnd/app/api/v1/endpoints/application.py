from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services import message_services as ms
from app.models.enums import ApplicationStatus
from app.schemas import ApplicationCreate, ApplicationRespond

router = APIRouter(prefix="/applications", tags=['申请'])


def format_application_response(app) -> dict:
    """格式化申请响应"""
    return {
        "id": app.id,
        "recruitment_id": app.recruitment_id,
        "applicant_id": app.applicant_id,
        "receiver_id": app.receiver_id,
        "status": app.status,
        "created_at": app.created_at,
        "applicant_name": app.applicant.username if app.applicant else None,
        "applicant_avatar": app.applicant.avatar_url if app.applicant else None,
        "recruitment_title": app.recruitment.title if app.recruitment else None,
        "receiver_name": app.receiver.username if app.receiver else None,
    }


@router.post("")
def send_application(
    data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    用户A向招募发起人发送申请
    """
    # 获取招募信息，找到接收者（招募发起人）
    from app.services import recruitment_services as rs
    recruitment = rs.get_recruitment_by_id(db, data.recruitment_id)
    if not recruitment:
        raise HTTPException(status_code=404, detail="招募不存在")

    # 不能向自己申请
    if recruitment.creator_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能申请自己的招募")

    application = ms.send_application(
        db=db,
        recruitment_id=data.recruitment_id,
        applicant_id=current_user.id,
        receiver_id=recruitment.creator_id
    )

    return {"message": "申请已发送", "application_id": application.id}


@router.get("/unread/count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取未读申请数量（红点）"""
    count = ms.get_unread_application_count(db, current_user.id)
    return {"unread_count": count}


@router.get("/received")
def get_received_applications(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    用户B/C 查看收到的申请
    """
    applications = ms.get_received_applications(db, current_user.id, status)
    return {
        "applications": [format_application_response(app) for app in applications]
    }


@router.get("/sent")
def get_sent_applications(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    查看自己发出的申请
    """
    applications = ms.get_sent_applications(db, current_user.id, status)
    return {
        "applications": [format_application_response(app) for app in applications]
    }


@router.get("/all")
def get_all_applications(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    用户D 在个人主页查看所有相关申请（分页）
    """
    applications = ms.get_all_user_applications(db, current_user.id, skip, limit)
    return {
        "total": len(applications),
        "skip": skip,
        "limit": limit,
        "applications": [format_application_response(app) for app in applications]
    }


@router.post("/{application_id}/respond")
def respond_to_application(
    application_id: int,
    data: ApplicationRespond,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    用户B 接受或拒绝申请
    """
    application = ms.respond_to_application(
        db=db,
        application_id=application_id,
        responder_id=current_user.id,
        accept=data.accept
    )

    if not application:
        raise HTTPException(status_code=404, detail="申请不存在或无权响应")

    action = "接受" if data.accept else "拒绝"
    return {"message": f"已{action}申请", "application_id": application_id}
