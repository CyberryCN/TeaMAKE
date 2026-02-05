from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services import team_services as ts

router = APIRouter(prefix="/teams", tags=['队伍'])


def format_team_response(team, members=None) -> dict:
    """格式化队伍响应"""
    if members is None:
        members = []
        for m in team.members:
            members.append({
                "user_id": m.user.id,
                "username": m.user.username,
                "avatar_url": m.user.avatar_url,
                "role": m.role,
                "joined_at": m.joined_at
            })

    return {
        "id": team.id,
        "name": team.name,
        "description": team.description,
        "competition_name": team.competition_name,
        "competition_url": team.competition_url,
        "is_active": team.is_active,
        "created_at": team.created_at,
        "members": members
    }


@router.get("/{team_id}")
def get_team_detail(
    team_id: int,
    db: Session = Depends(get_db)
):
    """获取队伍详情"""
    team = ts.get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="队伍不存在")

    return format_team_response(team)


@router.get("/recruitment/{recruitment_id}")
def get_team_by_recruitment(
    recruitment_id: int,
    db: Session = Depends(get_db)
):
    """根据招募ID获取队伍"""
    team = ts.get_team_by_recruitment(db, recruitment_id)
    if not team:
        raise HTTPException(status_code=404, detail="队伍不存在")

    return format_team_response(team)


@router.get("/my/list")
def get_my_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我加入的所有队伍"""
    teams = ts.get_user_teams(db, current_user.id)
    return {
        "teams": [format_team_response(team) for team in teams]
    }


@router.post("/{team_id}/members/{user_id}")
def add_team_member(
    team_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加队伍成员"""
    team = ts.get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="队伍不存在")

    # 只有队长可以添加成员
    is_leader = any(
        m.user_id == current_user.id and m.role == "leader"
        for m in team.members
    )
    if not is_leader:
        raise HTTPException(status_code=403, detail="只有队长可以添加成员")

    member = ts.add_team_member(db, team_id, user_id)
    return {"message": "添加成功"}


@router.delete("/{team_id}/members/{user_id}")
def remove_team_member(
    team_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """移除队伍成员"""
    team = ts.get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="队伍不存在")

    # 只有队长可以移除成员
    is_leader = any(
        m.user_id == current_user.id and m.role == "leader"
        for m in team.members
    )
    if not is_leader:
        raise HTTPException(status_code=403, detail="只有队长可以移除成员")

    success = ts.remove_team_member(db, team_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="成员不存在")

    return {"message": "移除成功"}
