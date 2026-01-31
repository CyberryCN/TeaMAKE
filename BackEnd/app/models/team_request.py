from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from datetime import datetime
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.enums import TeamRequestStatus


class TeamRequest(Base):
    """组队请求表 - 用于申请加入招募"""
    __tablename__ = "team_request"

    id = Column(Integer, primary_key=True, index=True)
    recruitment_id = Column(Integer, ForeignKey("recruitment.id"), index=True)
    requester_id = Column(Integer, ForeignKey("user.id"), index=True)  # 发起请求者
    receiver_id = Column(Integer, ForeignKey("user.id"), index=True)   # 接收请求者

    message = Column(Text, nullable=True)  # 申请附言
    status = Column(String(20), default=TeamRequestStatus.PENDING.value, index=True)

    # 消息状态
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    handled_at = Column(DateTime, nullable=True)

    # 关系
    recruitment = relationship("Recruitment", back_populates="requests")
    requester = relationship("User", back_populates="sent_requests", foreign_keys=[requester_id])
    receiver = relationship("User", back_populates="received_requests", foreign_keys=[receiver_id])
