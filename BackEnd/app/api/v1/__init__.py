from fastapi import APIRouter
from app.api.v1.endpoints import user, admin_skill, skill, recruitment

router = APIRouter()
router.include_router(user.router)
router.include_router(admin_skill.router)
router.include_router(skill.router)
router.include_router(recruitment.router)
