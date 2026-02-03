from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from app.models.user import User
from app.services import user_services as us
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, UserUpdate,
    AuthRequest, AuthResponse, LoginResponse,
    UpdatePasswordRequest, MessageResponse, UserSkillAdd
)

router = APIRouter(prefix="/users", tags=['用户'])


@router.post("/register", response_model=MessageResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    try:
        user = us.register_user(
            db, data.username, data.QQ_num, data.email, data.password, data.college
        )
        return {"msg": "注册成功", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth", response_model=AuthResponse)
def auth(data: AuthRequest, db: Session = Depends(get_db)):
    """学信网验证"""
    try:
        result = us.auth_user(
            db, data.user_id, data.chsi_code
        )
        if result['success']:
            return {"msg": "验证成功", "detail": result.get("message")}
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """通过user_id获取用户信息（不含敏感字段）"""
    user = us.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.get("/{user_id}/detail")
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    """获取用户详细信息（含技能和经历）"""
    user = us.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "college": user.college,
        "QQ_num": user.QQ_num,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "phone": user.phone,
        "authenticated": user.authenticated,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "last_login_at": user.last_login_at,
        "skills": [{
            "id": s.id,
            "name": s.name,
            "category_id": s.category_id,
            "category_name": s.category.name if s.category else ""
        } for s in user.skills],
        "experiences": []
    }


@router.post("/login", response_model=LoginResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = us.authenticate_user(
        db, data.username, data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="用户名不存在或密码错误")

    # 更新最后登录时间
    us.update_last_login(db, user.id)

    # 生成 JWT Token
    token_data = {"sub": user.id, "username": user.username}
    access_token = create_access_token(token_data)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "college": user.college,
        "token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.put("/{user_id}/profile", response_model=MessageResponse)
def update_profile(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    """修改个人资料"""
    try:
        user = us.update_profile(
            db, user_id, data.bio, data.avatar_url, data.phone, data.college
        )
        return {"msg": "修改成功", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}/password")
def update_password(user_id: int, data: UpdatePasswordRequest, db: Session = Depends(get_db)):
    """修改密码"""
    try:
        result = us.update_password(db, user_id, data.old_password, data.new_password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}/skills", response_model=MessageResponse)
def update_user_skills(user_id: int, data: UserSkillAdd, db: Session = Depends(get_db)):
    """更新用户技能标签"""
    try:
        skills = us.update_user_skills(db, user_id, data.skill_ids)
        return {"msg": f"已更新 {len(skills)} 个技能", "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息（需要登录）"""
    return current_user
