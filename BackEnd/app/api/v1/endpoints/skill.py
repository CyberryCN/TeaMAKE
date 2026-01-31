from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import skill_services as ss
from app.schemas.skill import SkillResponse, UserSkillAdd, UserSkillResponse
from app.schemas.user import MessageResponse
from app.models.user import User

router = APIRouter(prefix="/skills", tags=['技能'])


@router.get("", response_model=list[SkillResponse])
def list_all_skills(db: Session = Depends(get_db)):
    """获取所有技能列表"""
    from app.models.skill import Skill
    skills = db.query(Skill).all()
    return [{
        "id": s.id,
        "name": s.name,
        "category_id": s.category_id,
        "category_name": s.category.name
    } for s in skills]


@router.get("/categories/{category_name}", response_model=list[SkillResponse])
def list_skills_by_category(category_name: str, db: Session = Depends(get_db)):
    """按分类获取技能列表"""
    skills = ss.get_skills_by_category(db, category_name)
    return [{
        "id": s.id,
        "name": s.name,
        "category_id": s.category_id,
        "category_name": s.category.name
    } for s in skills]


@router.get("/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    """获取所有分类名称（简单列表）"""
    categories = ss.get_all_categories(db)
    return [c.name for c in categories]


@router.get("/user/{user_id}", response_model=UserSkillResponse)
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    """获取用户的技能列表"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return {
        "user_id": user_id,
        "skills": [{
            "id": s.id,
            "name": s.name,
            "category_id": s.category_id,
            "category_name": s.category.name
        } for s in user.skills]
    }


@router.post("/user/{user_id}", response_model=MessageResponse)
def add_skills_to_user(user_id: int, data: UserSkillAdd, db: Session = Depends(get_db)):
    """为用户添加技能（从管理员预设的技能列表中选择）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    from app.models.skill import Skill
    skills = db.query(Skill).filter(Skill.id.in_(data.skill_ids)).all()

    # 检查是否所有ID都找到了对应的技能
    found_ids = {s.id for s in skills}
    not_found_ids = set(data.skill_ids) - found_ids
    if not_found_ids:
        raise HTTPException(
            status_code=400,
            detail=f"以下技能ID不存在: {sorted(not_found_ids)}"
        )

    # 添加技能到用户（自动处理关联表）
    for skill in skills:
        if skill not in user.skills:
            user.skills.append(skill)

    db.commit()
    return {"msg": f"成功添加 {len(skills)} 个技能到用户"}


@router.delete("/user/{user_id}", response_model=MessageResponse)
def remove_skills_from_user(user_id: int, data: UserSkillAdd, db: Session = Depends(get_db)):
    """从用户移除技能"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    from app.models.skill import Skill
    skills = db.query(Skill).filter(Skill.id.in_(data.skill_ids)).all()

    removed_count = 0
    for skill in skills:
        if skill in user.skills:
            user.skills.remove(skill)
            removed_count += 1

    db.commit()
    return {"msg": f"成功移除 {removed_count} 个技能"}
