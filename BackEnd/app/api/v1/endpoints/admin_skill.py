from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import skill_services as ss
from app.schemas.skill import (
    CategoryCreate, CategoryResponse, CategoryWithSkillsResponse,
    SkillCreate, SkillResponse, UserSkillAdd, UserSkillResponse
)
from app.schemas.user import MessageResponse

router = APIRouter(prefix="/admin/skills", tags=['管理员-技能管理'])


@router.post("/categories", response_model=CategoryResponse)
def add_category(data: CategoryCreate, db: Session = Depends(get_db)):
    """添加技能分类（支持中文，如"后端开发"）"""
    try:
        category = ss.admin_add_category(db, data.name, data.description)
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "created_at": category.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """获取所有技能分类"""
    categories = ss.get_all_categories(db)
    return [{
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "created_at": c.created_at.isoformat()
    } for c in categories]


@router.post("", response_model=SkillResponse)
def add_skill(data: SkillCreate, db: Session = Depends(get_db)):
    """添加技能标签（需要指定已存在的分类）"""
    try:
        skill = ss.admin_add_skill(db, data.name, data.category_name)
        return {
            "id": skill.id,
            "name": skill.name,
            "category_id": skill.category_id,
            "category_name": skill.category.name
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[SkillResponse])
def list_skills(db: Session = Depends(get_db)):
    """获取所有技能"""
    from app.models.skill import Skill
    skills = db.query(Skill).all()
    return [{
        "id": s.id,
        "name": s.name,
        "category_id": s.category_id,
        "category_name": s.category.name
    } for s in skills]


@router.get("/categories/{category_name}/skills", response_model=list[SkillResponse])
def list_skills_by_category(category_name: str, db: Session = Depends(get_db)):
    """获取指定分类下的所有技能"""
    skills = ss.get_skills_by_category(db, category_name)
    return [{
        "id": s.id,
        "name": s.name,
        "category_id": s.category_id,
        "category_name": s.category.name
    } for s in skills]
