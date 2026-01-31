from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship


class SkillCategory(Base):
    """技能分类表（如：后端, 前端, 算法, 设计）"""
    __tablename__ = "skill_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)  # 分类名，支持中文
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 关系
    skills = relationship("Skill", back_populates="category", cascade="all, delete-orphan")


class Skill(Base):
    """技能标签表"""
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    category_id = Column(Integer, ForeignKey("skill_category.id"))  # 外键不需要额外index
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 关系
    category = relationship("SkillCategory", back_populates="skills")
