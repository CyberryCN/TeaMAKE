from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# ============ 用户相关schemas ============

class UserBase(BaseModel):
    """用户基础信息"""
    username: str
    email: EmailStr
    college: str


class UserCreate(UserBase):
    """注册请求"""
    QQ_num: int
    password: str


class UserLogin(BaseModel):
    """登录请求"""
    username: str
    password: str


class UserResponse(UserBase):
    """用户响应（不包含敏感信息）"""
    id: int
    QQ_num: int
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    authenticated: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """更新用户资料"""
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    college: Optional[str] = None


class UpdatePasswordRequest(BaseModel):
    """修改密码"""
    old_password: str
    new_password: str


# ============ 竞赛经历相关schemas ============

class ExperienceBase(BaseModel):
    """竞赛经历基础"""
    competition_name: str
    competition_level: str  # 校级, 省级, 国家级, 国际级
    role: str  # 队长, 核心成员, 普通成员
    start_time: datetime


class ExperienceCreate(ExperienceBase):
    """创建竞赛经历"""
    award_level: Optional[str] = None
    award_name: Optional[str] = None
    description: Optional[str] = None
    end_time: Optional[datetime] = None
    certificate_url: Optional[str] = None


class ExperienceResponse(BaseModel):
    """竞赛经历响应"""
    id: int
    user_id: int
    competition_name: str
    competition_level: str
    role: str
    start_time: datetime
    award_level: Optional[str] = None
    award_name: Optional[str] = None
    description: Optional[str] = None
    end_time: Optional[datetime] = None
    certificate_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Auth相关schemas ============

class AuthRequest(BaseModel):
    """学信网验证请求"""
    user_id: int
    chsi_code: str


class AuthResponse(BaseModel):
    """验证响应"""
    msg: str
    detail: Optional[str] = None


class LoginResponse(BaseModel):
    """登录成功响应"""
    id: int
    username: str
    email: str
    college: str
    token: str  # 后续添加JWT后使用


class MessageResponse(BaseModel):
    """通用消息响应"""
    msg: str
    user_id: Optional[int] = None


class UserSkillAdd(BaseModel):
    """用户添加技能请求"""
    skill_ids: List[int]
