from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, UniqueConstraint
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.enums import MessageType, ApplicationStatus


class Conversation(Base):
    """私聊会话表"""
    __tablename__ = "conversation"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("user.id"), index=True)
    user2_id = Column(Integer, ForeignKey("user.id"), index=True)

    # 关联到招募（可选）
    recruitment_id = Column(Integer, ForeignKey("recruitment.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # 关系
    user1 = relationship("User", back_populates="conversations", foreign_keys=[user1_id])
    user2 = relationship("User", back_populates="conversations_as_user2", foreign_keys=[user2_id])
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uix_conversation_user_pair"),
    )


class Message(Base):
    """消息表"""
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"), index=True)
    sender_id = Column(Integer, ForeignKey("user.id"), index=True)

    content = Column(Text)
    message_type = Column(String(20), default=MessageType.TEXT.value)

    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 关系
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User")

class Application(Base):
    """组队申请"""
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, index=True)
    recruitment_id = Column(Integer, ForeignKey("recruitment.id"), index=True)
    applicant_id = Column(Integer, ForeignKey("user.id"), index=True)  # 申请人
    receiver_id = Column(Integer, ForeignKey("user.id"), index=True)   # 接收者（通常是招募发起人）

    status = Column(String, default=ApplicationStatus.WAITING.value)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 关系（使用 foreign_keys 明确指定外键）
    applicant = relationship("User", foreign_keys=[applicant_id], back_populates="sent_applications")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_applications")
    recruitment = relationship("Recruitment", back_populates="applications")
    