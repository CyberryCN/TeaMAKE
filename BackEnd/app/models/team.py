from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship


class Team(Base):
    """组队/队伍表 - 确认组队后创建"""
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    recruitment_id = Column(Integer, ForeignKey("recruitment.id"), unique=True, nullable=True)

    name = Column(String(100), index=True)  # 队伍名称
    description = Column(Text, nullable=True)
    competition_name = Column(String(100), index=True)
    competition_url = Column(String(500), nullable=True)

    # 队伍状态
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # 关系
    recruitment = relationship("Recruitment", back_populates="team")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    users = relationship("User", secondary="team_member", viewonly=True)

    # 队伍专属私聊
    chat_room_id = Column(Integer, ForeignKey("conversation.id"), nullable=True)
    chat_room = relationship("Conversation", foreign_keys=[chat_room_id])


class TeamMember(Base):
    """队伍成员关联表"""
    __tablename__ = "team_member"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)

    role = Column(String(50), default="member")  # 队长: leader, 成员: member
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    # 复合唯一约束
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uix_team_member_team_user"),
    )

    # 关系
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")
