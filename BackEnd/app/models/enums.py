from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from datetime import datetime
import enum
from app.core.database import Base


class RecruitStatus(enum.Enum):
    DRAFT = "draft"           # 草稿
    OPEN = "open"             # 开放中
    FULL = "full"             # 已满员
    CLOSED = "closed"         # 已关闭
    COMPLETED = "completed"   # 已完成


class TeamRequestStatus(enum.Enum):
    PENDING = "pending"       # 待处理
    ACCEPTED = "accepted"     # 已接受
    REJECTED = "rejected"     # 已拒绝
    CANCELLED = "cancelled"   # 已取消


class MessageType(enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
