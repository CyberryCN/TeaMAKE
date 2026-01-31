from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.skill import Skill, SkillCategory


def get_all_categories(db: Session):
    """获取所有技能分类"""
    return db.query(SkillCategory).all()


def get_category_by_name(db: Session, name: str) -> SkillCategory | None:
    """根据名称获取分类"""
    return db.query(SkillCategory).filter(SkillCategory.name == name).first()


def admin_add_category(db: Session, name: str, description: str = None) -> SkillCategory:
    """
    管理员添加技能分类

    Args:
        db: 数据库会话
        name: 分类名称（支持中文，如"后端开发"、"前端开发"）
        description: 分类描述

    Returns:
        创建的 SkillCategory 对象

    Raises:
        ValueError: 分类已存在
    """
    if get_category_by_name(db, name):
        raise ValueError(f"分类 '{name}' 已存在")

    category = SkillCategory(
        name=name,
        description=description
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def admin_add_skill(db: Session, name: str, category_name: str):
    """
    管理员添加技能标签

    Args:
        db: 数据库会话
        name: 技能名称
        category_name: 分类名称（必须是已存在的分类）

    Returns:
        创建的 Skill 对象

    Raises:
        ValueError: 技能已存在 / 分类不存在
    """
    # 检查技能是否已存在
    if db.query(Skill).filter(Skill.name == name).first():
        raise ValueError(f"技能 '{name}' 已存在")

    # 检查分类是否存在
    category = get_category_by_name(db, category_name)
    if not category:
        raise ValueError(
            f"分类 '{category_name}' 不存在，请先调用 /admin/categories 接口添加分类"
        )

    skill = Skill(
        name=name,
        category_id=category.id
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def get_skills_by_category(db: Session, category_name: str):
    """获取指定分类下的所有技能"""
    category = get_category_by_name(db, category_name)
    if not category:
        return []
    return db.query(Skill).filter(Skill.category_id == category.id).all()


def get_user_skills(db: Session, user_id: int):
    """获取用户的所有技能（需要配合user模型的关系）"""
    # 这里需要根据user模型的关系来查询
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    return user.skills
