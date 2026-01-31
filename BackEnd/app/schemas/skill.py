from pydantic import BaseModel
from typing import Optional, List


# ============ 技能分类 Schemas ============

class CategoryCreate(BaseModel):
    """创建分类请求"""
    name: str  # 支持中文，如"后端开发"
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    """分类响应"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: str  # 转换为字符串方便前端显示

    class Config:
        from_attributes = True


class CategoryWithSkillsResponse(CategoryResponse):
    """分类及其下的技能列表"""
    skills: List["SkillResponse"] = []


# ============ 技能 Schemas ============

class SkillCreate(BaseModel):
    """创建技能请求"""
    name: str  # 技能名称
    category_name: str  # 分类名称（不是ID，方便管理员使用）


class SkillResponse(BaseModel):
    """技能响应"""
    id: int
    name: str
    category_id: int
    category_name: str  # 分类名称（方便前端显示）

    class Config:
        from_attributes = True


# ============ 用户技能 Schemas ============

class UserSkillAdd(BaseModel):
    """用户添加技能请求"""
    skill_ids: List[int]  # 技能ID列表


class UserSkillResponse(BaseModel):
    """用户技能响应"""
    user_id: int
    skills: List[SkillResponse]
