from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ApplicationResponse(BaseModel):
    """申请响应"""
    id: int
    recruitment_id: int
    applicant_id: int
    receiver_id: int
    status: str
    created_at: datetime

    # 关联信息
    applicant_name: Optional[str] = None
    applicant_avatar: Optional[str] = None
    recruitment_title: Optional[str] = None
    receiver_name: Optional[str] = None


class ApplicationListResponse(BaseModel):
    """申请列表响应"""
    total: int
    applications: List[ApplicationResponse]


class ApplicationMessageResponse(BaseModel):
    """申请操作消息响应"""
    message: str
    application_id: Optional[int] = None


class ApplicationCreate(BaseModel):
    """发送申请"""
    recruitment_id: int


class ApplicationRespond(BaseModel):
    """响应申请"""
    accept: bool
