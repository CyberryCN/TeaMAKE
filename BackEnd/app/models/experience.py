from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship


class CompetitionExperience(Base):
    """竞赛经历表"""
    __tablename__ = "competition_experience"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)

    competition_name = Column(String(100))
    competition_level = Column(String(20))  # 校级, 省级, 国家级, 国际级
    award_level = Column(String(20), nullable=True)  # 一等奖, 二等奖, 三等奖, 优秀奖
    award_name = Column(String(100), nullable=True)  # 如：国家一等奖
    role = Column(String(50))  # 担任角色：队长, 核心成员, 普通成员
    description = Column(Text, nullable=True)  # 具体负责内容
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    certificate_url = Column(String(500), nullable=True)  # 证书图片URL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 关系
    user = relationship("User", back_populates="experiences")
