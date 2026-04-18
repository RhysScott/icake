from sqlalchemy.orm import Session
from database import User
from domain.vo import (
    UserLoginRequest,
    UserRegisterRequest,
    UserPasswordResetRequest,
    UserUpdateRequest
)
from domain.dto import JwtPayload
from utils import PasswordHasher, JwtUtil, DateTimeUtils, CacheUtils
from exception import BusinessException
from constant import CacheKey


class UserService:
    """用户服务类
    提供用户注册、登录、信息修改、密码重置等核心业务逻辑
    """

    @staticmethod
    def get(db: Session, phone: str) -> User | None:
        """根据手机号查询用户
        只查询未被逻辑删除的用户
        """
        # 根据手机号查询未删除的用户
        return db.query(User).filter(User.phone == phone, User.is_deleted == 0).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        """根据用户ID查询用户
        只查询未被逻辑删除的用户
        """
        # 根据用户ID查询未删除的用户
        return db.query(User).filter(User.id == user_id, User.is_deleted == 0).first()

    @staticmethod
    def register(db: Session, req: UserRegisterRequest) -> User:
        """用户注册
        检查手机号是否已存在，密码加密后保存用户信息
        """
        # 检查手机号是否已注册
        exist_user = UserService.get(db, req.phone)
        if exist_user:
            raise BusinessException("该手机号已注册")

        # 密码加密
        password_hash = PasswordHasher.hash(req.password)

        # 构建用户对象
        user = User(
            phone=req.phone,
            password=password_hash,
            nickname=req.nickname
        )

        # 保存到数据库
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, req: UserLoginRequest) -> tuple[str, User]:
        """用户登录
        验证账号密码，生成JWT令牌
        """
        # 查询用户是否存在
        user = UserService.get(db, req.phone)
        if not user:
            raise BusinessException("账号或密码错误")

        # 校验密码
        if not PasswordHasher.verify(req.password, user.password):  # type: ignore
            raise BusinessException("账号或密码错误")

        # 生成 JWT 载荷
        payload = JwtPayload(
            user_id=user.id, # type:ignore
            iat=DateTimeUtils.now(),
            exp=DateTimeUtils.expire()
        )  # type: ignore

        # 生成 token
        token = JwtUtil.encode(payload)
        return token, user

    @staticmethod
    def reset_password(db: Session, req: UserPasswordResetRequest) -> User:
        """重置用户密码
        验证验证码有效性，更新密码并清除缓存
        """
        # 检查用户是否存在
        user = UserService.get(db, req.phone)
        if not user:
            raise BusinessException("用户不存在")

        # 校验验证码是否正确
        cache_key = CacheKey.reset_password_code(req.phone)
        cache_code = CacheUtils.get(cache_key)
        if not cache_code or cache_code != req.code:
            raise BusinessException("验证码错误或已过期")

        # 更新密码
        user.password = PasswordHasher.hash(req.password)  # type: ignore
        db.commit()

        # 清除验证码缓存
        CacheUtils.delete(cache_key)
        return user

    @staticmethod
    def update_info(db: Session, user_id: int, req: UserUpdateRequest) -> User:
        """更新用户基本信息
        支持修改昵称、头像、性别、生日、个人简介
        """
        # 查询要更新的用户
        user = UserService.get_by_id(db, user_id)
        if not user:
            raise BusinessException("用户不存在")

        # 逐个更新允许修改的字段
        if req.nickname is not None:
            user.nickname = req.nickname  # type: ignore
        if req.avatar_url is not None:
            user.avatar_url = req.avatar_url  # type: ignore
        if req.gender is not None:
            user.gender = req.gender  # type: ignore
        if req.birthday is not None:
            user.birthday = req.birthday  # type: ignore
        if req.bio is not None:
            user.bio = req.bio  # type: ignore

        # 提交并刷新
        db.commit()
        db.refresh(user)
        return user
