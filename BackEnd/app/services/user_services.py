from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User
from chsi import verify
from app.core.security import get_password_hash, verify_password


def register_user(db: Session, username: str, QQ_num: int, email: str, password: str, college: str):
    """
    注册新用户

    Args:
        db: 数据库会话
        username: 用户名
        QQ_num: QQ号
        email: 邮箱
        password: 密码（明文）
        college: 学校

    Returns:
        创建的 User 对象

    Raises:
        ValueError: 用户名/QQ/邮箱已存在
    """
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == username).first():
        raise ValueError("用户名已存在")

    # 检查 QQ 号是否已存在
    if db.query(User).filter(User.QQ_num == QQ_num).first():
        raise ValueError("QQ号已注册")

    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == email).first():
        raise ValueError("邮箱已注册")

    # 创建用户
    user = User(
        username=username,
        QQ_num=QQ_num,
        email=email,
        hashed_password=get_password_hash(password),
        college=college,
        authenticated=False,  # 默认未验证学信网
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def auth_user(db: Session, user_id: int, chsi_code: str) -> dict:
    """
    学信网验证

    Args:
        db: 数据库会话
        user_id: 用户ID
        chsi_code: 16位学信网验证码

    Returns:
        验证结果字典 {"success": bool, "message": str}

    Raises:
        ValueError: 用户不存在或验证码无效
    """
    # 检查用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("用户不存在")

    if len(chsi_code) != 16:
        raise ValueError("验证码应为16位")

    # 调用学信网验证
    result = verify(chsi_code, lang="CN")

    # 根据返回的 status 字段判断验证结果
    # status 为 True 表示验证成功
    if result.get("status") is True:
        user.authenticated = True
        db.commit()
        return {"success": True, "message": "学信网验证成功"}
    else:
        # 记录验证失败原因（如果有）
        error_msg = result.get("message", "学信网验证失败，请检查验证码")
        return {"success": False, "message": error_msg}


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """根据用户名获取用户"""
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    用户登录验证

    Args:
        db: 数据库会话
        username: 用户名
        password: 密码（明文）

    Returns:
        验证成功返回 User 对象，失败返回 None
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_last_login(db: Session, user_id: int):
    """更新最后登录时间"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.last_login_at = datetime.now(timezone.utc)
        db.commit()


def update_profile(
    db: Session,
    user_id: int,
    bio: str = None,
    avatar_url: str = None,
    phone: str = None,
    college: str = None
) -> User:
    """
    修改个人资料

    Args:
        db: 数据库会话
        user_id: 用户ID
        bio: 个人简介
        avatar_url: 头像URL
        phone: 联系电话
        college: 学校

    Returns:
        更新后的 User 对象

    Raises:
        ValueError: 用户不存在
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("用户不存在")

    # 只更新传入的字段
    if bio is not None:
        user.bio = bio
    if avatar_url is not None:
        user.avatar_url = avatar_url
    if phone is not None:
        user.phone = phone
    if college is not None:
        user.college = college

    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session, user_id: int, old_password: str, new_password: str) -> dict:
    """
    修改密码

    Args:
        db: 数据库会话
        user_id: 用户ID
        old_password: 旧密码（明文）
        new_password: 新密码（明文）

    Returns:
        {"success": True, "message": "密码修改成功"}

    Raises:
        ValueError: 用户不存在或旧密码错误
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("用户不存在")

    # 验证旧密码
    if not verify_password(old_password, user.hashed_password):
        raise ValueError("旧密码错误")

    # 设置新密码
    user.hashed_password = get_password_hash(new_password)
    db.commit()

    return {"success": True, "message": "密码修改成功"}


def update_user_skills(db: Session, user_id: int, skill_ids: list):
    """
    更新用户的技能标签

    Args:
        db: 数据库会话
        user_id: 用户ID
        skill_ids: 技能ID列表

    Returns:
        更新后的用户技能列表

    Raises:
        ValueError: 用户不存在
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("用户不存在")

    from app.models.skill import Skill
    skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()

    # 替换用户的技能
    user.skills = skills
    db.commit()
    db.refresh(user)

    return user.skills
