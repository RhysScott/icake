from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Text, DECIMAL
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from datetime import datetime
from common.settings import app_settings
from common.utils import Logger


Logger.info(f"数据库链接: {app_settings.db.db_url}")
# 数据库引擎
engine = create_engine(app_settings.db.db_url, echo=app_settings.db.echo)

# 基础模型
class Base(DeclarativeBase):
    pass

# 用户表
class AdminUser(Base):
    __tablename__ = "sys_user"

    id              = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username           = Column(String(36), unique=True, nullable=False, comment="用户名")
    password        = Column(String(64), nullable=False, comment="密码")
    avatar_url      = Column(String(255), nullable=True, comment="头像URL")
    bio             = Column(String(200), nullable=True, comment="个人简介")
    status          = Column(Integer, default=1, comment="状态：1正常 0禁用")
    is_deleted      = Column(Integer, default=0, comment="软删除")
    last_login_time = Column(DateTime, nullable=True, comment="最后登录时间")
    create_time     = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time     = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


# 用户表
class User(Base):
    __tablename__ = "user"

    id              = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    phone           = Column(String(11), unique=True, nullable=False, comment="手机号")
    password        = Column(String(64), nullable=False, comment="密码")
    nickname        = Column(String(32), nullable=True, comment="用户昵称")
    avatar_url      = Column(String(255), nullable=True, comment="头像URL")
    bio             = Column(String(200), nullable=True, comment="个人简介")
    gender          = Column(Integer, default=0, comment="性别：0未知 1男 2女")
    birthday        = Column(Date, nullable=True, comment="生日")
    status          = Column(Integer, default=1, comment="状态：1正常 0禁用")
    is_deleted      = Column(Integer, default=0, comment="软删除")
    last_login_time = Column(DateTime, nullable=True, comment="最后登录时间")
    create_time     = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time     = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

# 图片表
class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    rel_id = Column(Integer, nullable=True, comment="关联ID")
    index = Column(Integer, comment="图片索引，记录图片顺序")
    type = Column(Integer, nullable=False, comment="图片类型")
    path = Column(String(255), nullable=True, comment="头像路径")
    create_time     = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time     = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

# 公告表
class Notice(Base):
    __tablename__ = "notice"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="公告ID")
    title = Column(String(100), nullable=False, comment="公告标题")
    content = Column(Text, nullable=False, comment="公告内容")
    # 公告状态：0=关闭 1=开启
    status = Column(Integer, default=1, comment="公告状态 0=关闭 1=开启")
    # 排序值，越小越靠前
    index = Column(Integer, default=0, comment="排序序号")
    
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 商品表
class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="商品ID")
    name = Column(String(100), nullable=False, comment="商品名称")
    price = Column(DECIMAL(10,2), nullable=False, comment="商品价格")
    stock = Column(Integer, default=0, comment="库存数量")
    intro = Column(String(255), nullable=True, comment="商品简介")
    content = Column(Text, nullable=True, comment="商品详情")
    # 状态 0=下架 1=上架
    status = Column(Integer, default=1, comment="状态 0=下架 1=上架")
    
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

# 创建表
Base.metadata.create_all(engine)

# 会话工厂
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
