from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.enums import RecruitStatus


# 关联表：招募需要的技能 (多对多)
recruitment_skills = Table(
    "recruitment_skills",
    Base.metadata,
    Column("recruitment_id", Integer, ForeignKey("recruitment.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skill.id"), primary_key=True)
)


class Recruitment(Base):
    """组队招募/委托表"""
    __tablename__ = "recruitment"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("user.id"), index=True)

    title = Column(String(200))  # 招募标题
    description = Column(Text)  # 详细描述
    competition_name = Column(String(100), index=True)  # 目标竞赛名称
    competition_url = Column(String(500), nullable=True)  # 竞赛链接

    # 招募需求
    required_number = Column(Integer, default=1)  # 需要人数
    current_number = Column(Integer, default=0)   # 当前人数

    status = Column(String(20), default=RecruitStatus.OPEN.value, index=True)
    deadline = Column(DateTime, nullable=True)  # 招募截止时间

    # 竞赛时间估算
    expected_start = Column(DateTime, nullable=True)
    expected_end = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # 关系
    creator = relationship("User", back_populates="my_recruitments", foreign_keys=[creator_id])
    required_skills = relationship("Skill", secondary=recruitment_skills)
    requests = relationship("TeamRequest", back_populates="recruitment", cascade="all, delete-orphan")
    team = relationship("Team", back_populates="recruitment", uselist=False)
