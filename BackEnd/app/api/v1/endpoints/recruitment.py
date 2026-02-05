from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services import recruitment_services as rs
from app.schemas import (
    RecruitmentCreate, RecruitmentDraft, RecruitmentResponse,
    RecruitmentListResponse, RecruitmentUpdate, RecruitmentMessageResponse
)

router = APIRouter(prefix="/recruitments", tags=['招募'])


@router.post("/publish", response_model=RecruitmentResponse)
def publish_recruitment(
    data: RecruitmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发布招募（需要登录）"""
    try:
        recruitment = rs.post_recruitment(
            db=db,
            user_id=current_user.id,
            title=data.title,
            description=data.description,
            competition_name=data.competition_name,
            competition_url=data.competition_url,
            required_number=data.required_number,
            deadline=data.deadline,
            expected_start=data.expected_start,
            expected_end=data.expected_end,
            required_skills=data.required_skills
        )
        return recruitment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/draft", response_model=RecruitmentResponse)
def save_draft(
    data: RecruitmentDraft,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """保存草稿（需要登录）"""
    try:
        recruitment = rs.draft_recruitment(
            db=db,
            user_id=current_user.id,
            title=data.title,
            description=data.description,
            competition_name=data.competition_name,
            competition_url=data.competition_url,
            required_number=data.required_number,
            deadline=data.deadline,
            expected_start=data.expected_start,
            expected_end=data.expected_end,
            required_skills=data.required_skills
        )
        return recruitment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=RecruitmentListResponse)
def get_recruitments(
    page: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    competition_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取招募列表（分页，可按状态和竞赛名称筛选）"""
    recruitments, total = rs.get_recruitments(
        db=db,
        page=page,
        page_size=page_size,
        status=status,
        competition_name=competition_name
    )

    # 转换为响应格式
    items = []
    for r in recruitments:
        items.append({
            "id": r.id,
            "creator_id": r.creator_id,
            "title": r.title,
            "description": r.description,
            "competition_name": r.competition_name,
            "competition_url": r.competition_url,
            "required_number": r.required_number,
            "current_number": r.current_number,
            "status": r.status,
            "deadline": r.deadline,
            "expected_start": r.expected_start,
            "expected_end": r.expected_end,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "creator_name": r.creator.username if r.creator else None,
            "creator_avatar": r.creator.avatar_url if r.creator else None,
            "required_skills": [{
                "id": s.id,
                "name": s.name,
                "category_name": s.category.name if s.category else None
            } for s in r.required_skills]
        })

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "recruitments": items
    }


@router.get("/{recruitment_id}", response_model=RecruitmentResponse)
def get_recruitment_detail(
    recruitment_id: int,
    db: Session = Depends(get_db)
):
    """获取招募详情"""
    recruitment = rs.get_recruitment_by_id(db, recruitment_id)
    if not recruitment:
        raise HTTPException(status_code=404, detail="招募不存在")

    # 获取队伍成员
    team_members = []
    if recruitment.team:
        for member in recruitment.team.members:
            team_members.append({
                "user_id": member.user.id,
                "username": member.user.username,
                "avatar_url": member.user.avatar_url,
                "role": member.role,
                "joined_at": member.joined_at
            })

    return {
        "id": recruitment.id,
        "creator_id": recruitment.creator_id,
        "title": recruitment.title,
        "description": recruitment.description,
        "competition_name": recruitment.competition_name,
        "competition_url": recruitment.competition_url,
        "required_number": recruitment.required_number,
        "current_number": recruitment.current_number,
        "status": recruitment.status,
        "deadline": recruitment.deadline,
        "expected_start": recruitment.expected_start,
        "expected_end": recruitment.expected_end,
        "created_at": recruitment.created_at,
        "updated_at": recruitment.updated_at,
        "creator_name": recruitment.creator.username if recruitment.creator else None,
        "creator_avatar": recruitment.creator.avatar_url if recruitment.creator else None,
        "required_skills": [{
            "id": s.id,
            "name": s.name,
            "category_name": s.category.name if s.category else None
        } for s in recruitment.required_skills],
        "team": {
            "id": recruitment.team.id if recruitment.team else None,
            "name": recruitment.team.name if recruitment.team else None,
            "members": team_members
        } if recruitment.team else None
    }


@router.put("/{recruitment_id}", response_model=RecruitmentResponse)
def update_recruitment(
    recruitment_id: int,
    data: RecruitmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新招募（需要登录，只能更新自己的招募）"""
    recruitment = rs.update_recruitment(
        db=db,
        recruitment_id=recruitment_id,
        user_id=current_user.id,
        title=data.title,
        description=data.description,
        competition_name=data.competition_name,
        competition_url=data.competition_url,
        required_number=data.required_number,
        deadline=data.deadline,
        expected_start=data.expected_start,
        expected_end=data.expected_end,
        required_skills=data.required_skills
    )
    if not recruitment:
        raise HTTPException(status_code=404, detail="招募不存在或无权修改")

    return recruitment


@router.post("/{recruitment_id}/publish", response_model=RecruitmentResponse)
def publish_draft_recruitment(
    recruitment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发布草稿（需要登录）"""
    recruitment = rs.publish_draft(db, recruitment_id, current_user.id)
    if not recruitment:
        raise HTTPException(status_code=400, detail="发布失败，请检查必填字段是否完整")
    return recruitment


@router.post("/{recruitment_id}/close", response_model=RecruitmentMessageResponse)
def close_recruitment(
    recruitment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """关闭招募（需要登录）"""
    recruitment = rs.close_recruitment(db, recruitment_id, current_user.id)
    if not recruitment:
        raise HTTPException(status_code=404, detail="招募不存在或无权操作")
    return {"message": "招募已关闭", "recruitment_id": recruitment_id}


@router.delete("/{recruitment_id}", response_model=RecruitmentMessageResponse)
def delete_recruitment(
    recruitment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除招募（需要登录，只能删除草稿）"""
    success = rs.delete_recruitment(db, recruitment_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="招募不存在或无权删除")
    return {"message": "删除成功", "recruitment_id": recruitment_id}


@router.get("/my/list")
def get_my_recruitments(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我发布的招募列表"""
    recruitments = rs.get_recruitments_by_user(db, current_user.id, status)
    return recruitments
