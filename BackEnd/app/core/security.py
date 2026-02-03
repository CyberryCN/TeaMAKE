from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User

# ==================== 配置 ====================

# JWT 配置
SECRET_KEY = "tea-make-jwt-secret-key-2025"  # 生产环境请使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天过期

# 密码加密配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 认证路由
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


# ==================== Token Schema ====================

class Token(BaseModel):
    """JWT Token 响应"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # 过期时间（秒）


class TokenData(BaseModel):
    """Token 中的数据"""
    user_id: Optional[int] = None
    username: Optional[str] = None


# ==================== 密码处理 ====================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


# ==================== JWT Token ====================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT Token

    Args:
        data: 要编码的数据（包含 user_id, username 等）
        expires_delta: 自定义过期时间

    Returns:
        JWT Token 字符串
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    解码 JWT Token

    Args:
        token: JWT Token 字符串

    Returns:
        TokenData 对象，包含 user_id 和 username

    Raises:
        JWTError: Token 无效或已过期
    """
    # 禁用 sub 字段验证，因为我们的 sub 可能是整数
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_sub": False})
    sub = payload.get("sub")
    user_id = int(sub) if sub else None
    username: str = payload.get("username")

    if user_id is None:
        raise JWTError("Token 中缺少用户ID")

    return TokenData(user_id=user_id, username=username)


# ==================== 依赖注入 ====================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户

    使用方式：
    @router.get("/me")
    def get_me(current_user: User = Depends(get_current_user)):
        return current_user

    Returns:
        当前登录的用户对象

    Raises:
        401: Token 无效或未登录
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证用户身份",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = decode_access_token(token)
        if token_data.user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_user_optional(
    token: Optional[str] = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/users/login", auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    可选的当前用户（未登录时返回 None）

    使用方式：
    @router.get("/public")
    def public_view(current_user: Optional[User] = Depends(get_current_user_optional)):
        if current_user:
            return {"message": f"欢迎回来, {current_user.username}"}
        return {"message": "欢迎，游客"}
    """
    if token is None:
        return None

    try:
        return get_current_user(token, db)
    except HTTPException:
        return None
