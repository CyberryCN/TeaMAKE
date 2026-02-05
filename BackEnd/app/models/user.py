from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


# 关联表：用户技能 (多对多)
user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skill.id"), primary_key=True)
)


class User(Base):
    """用户表"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    QQ_num = Column(Integer, unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    college = Column(String(100))

    # 扩展字段
    bio = Column(Text, nullable=True)                               # 个人简介
    avatar_url = Column(String(500), nullable=True)                 # 头像URL
    phone = Column(String(20), nullable=True)                       # 联系电话
    authenticated = Column(Boolean, default=False, nullable=True)   # 学信网验证（通过post方法进行注册时候不需要认证，但是进行更多操作时候，需要在auth/register进行验证后才能进行）
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login_at = Column(DateTime, nullable=True)
    skills = relationship("Skill", secondary=user_skills)
    experiences = relationship("CompetitionExperience", back_populates="user")
    my_recruitments = relationship("Recruitment", back_populates="creator", foreign_keys="Recruitment.creator_id")
    sent_requests = relationship("TeamRequest", back_populates="requester", foreign_keys="TeamRequest.requester_id")
    received_requests = relationship("TeamRequest", back_populates="receiver", foreign_keys="TeamRequest.receiver_id")
    team_memberships = relationship("TeamMember", back_populates="user")
    conversations = relationship("Conversation", back_populates="user1", foreign_keys="Conversation.user1_id")
    conversations_as_user2 = relationship("Conversation", back_populates="user2", foreign_keys="Conversation.user2_id")
    sent_applications = relationship("Application", back_populates="applicant", foreign_keys="Application.applicant_id")
    received_applications = relationship("Application", back_populates="receiver", foreign_keys="Application.receiver_id")
