from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator, ConfigDict


class RecruitmentSkill(BaseModel):
    """关联技能详情"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category_name: Optional[str] = None


class RecruitmentBase(BaseModel):
    """招募基础字段"""
    title: Optional[str] = None
    description: Optional[str] = None
    competition_name: Optional[str] = None
    competition_url: Optional[str] = None
    required_number: int = 1


class RecruitmentCreate(RecruitmentBase):
    """发布招募 - 严格验证"""
    title: str
    description: str
    competition_name: str
    required_number: int
    deadline: datetime
    expected_start: datetime
    expected_end: datetime
    required_skills: List[int] = []

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('标题不能为空')
        return v.strip()

    @field_validator('required_number')
    @classmethod
    def required_number_positive(cls, v):
        if v < 1:
            raise ValueError('招募人数必须大于0')
        return v


class RecruitmentDraft(RecruitmentBase):
    """草稿 - 可选验证"""
    deadline: Optional[datetime] = None
    expected_start: Optional[datetime] = None
    expected_end: Optional[datetime] = None
    required_skills: List[int] = []


class RecruitmentResponse(BaseModel):
    """招募响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    competition_name: Optional[str] = None
    competition_url: Optional[str] = None
    required_number: int
    current_number: int
    status: str
    deadline: Optional[datetime] = None
    expected_start: Optional[datetime] = None
    expected_end: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    # 关联信息
    creator_name: Optional[str] = None
    creator_avatar: Optional[str] = None
    required_skills: List[RecruitmentSkill] = []


class RecruitmentListResponse(BaseModel):
    """招募列表响应"""
    total: int
    page: int
    page_size: int
    recruitments: List[RecruitmentResponse]


class RecruitmentUpdate(BaseModel):
    """更新招募"""
    title: Optional[str] = None
    description: Optional[str] = None
    competition_name: Optional[str] = None
    competition_url: Optional[str] = None
    required_number: Optional[int] = None
    deadline: Optional[datetime] = None
    expected_start: Optional[datetime] = None
    expected_end: Optional[datetime] = None
    required_skills: Optional[List[int]] = None


class RecruitmentMessageResponse(BaseModel):
    """招募操作消息响应"""
    message: str
    recruitment_id: Optional[int] = None
