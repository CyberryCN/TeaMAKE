from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# 数据库连接配置
DATABASE_URL = "sqlite:///./tea_make.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话的依赖函数

    使用方式：
    @app.get("/users")
    def get_users(db: Session = Depends(get_db)):
        users = db.query(User).all()
        return users

    FastAPI 会自动管理会话的生命周期：
    1. 请求开始时创建会话
    2. 请求处理中使用会话
    3. 请求结束时关闭会话（即使发生异常）
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    创建所有数据库表

    使用方法：
    1. 在第一次运行应用时调用
    2. 或者在数据库迁移时使用
    """
    print("正在创建数据库表...")

    # 关闭所有连接并删除数据库文件
    global engine, SessionLocal
    engine.dispose()

    db_path = "tea_make.db"
    wal_path = db_path + "-wal"
    shm_path = db_path + "-shm"

    import os
    for path in [db_path, wal_path, shm_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"已删除: {path}")

    # 重新创建 engine 和 session
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 重新创建表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")

def test_connection():
    """测试数据库连接是否正常"""
    try:
        with engine.connect() as conn:
            print("✓ 数据库连接成功")
            return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False

# 如果直接运行这个文件，会初始化数据库
if __name__ == "__main__":
    init_db()
    test_connection()