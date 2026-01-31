import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db, test_connection
from app.api.v1 import router as api_v1
# 导入所有模型，确保它们被注册到 Base.metadata
from app.models import User, Skill, SkillCategory, CompetitionExperience, Recruitment, TeamRequest, Team, TeamMember, Conversation, Message

app = FastAPI(
    title="TeaMAKE - 大学生竞赛组队平台",
    description="提供线上竞赛组队、委托发布、私聊功能",
    version="1.0.0"
)

# 配置 CORS，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
init_db()
test_connection()

# 注册路由
app.include_router(api_v1, prefix="/api/v1")


@app.get("/")
def root():
    """根路径"""
    return {"message": "Welcome to TeaMAKE API", "docs": "/docs"}


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "ok"}
