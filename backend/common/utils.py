import bcrypt
import jwt
from domain.dto import JwtPayload
from common.settings import app_settings
from datetime import datetime, timedelta
import redis
import logging
import os


class Logger:
    """统一日志工具类"""

    # 日志存放目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 按日期生成当天日志文件
    log_file = os.path.join(log_dir, f"icake_{datetime.now().strftime('%Y-%m-%d')}.log")

    # 获取日志对象并设置级别
    logger = logging.getLogger("icake")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # 避免重复添加处理器导致日志重复打印
    if not logger.handlers:
        # 控制台输出配置
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(asctime)s | %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # 文件输出配置，记录更详细的信息
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    @staticmethod
    def info(msg: str) -> None:
        """输出普通信息日志"""
        # 日志级别居中显示，宽度6
        level = " INFO ".center(6)
        Logger.logger.info(f"{level} | {msg}", stacklevel=2)

    @staticmethod
    def error(msg: str) -> None:
        """输出错误日志"""
        level = "ERROR".center(6)
        Logger.logger.error(f"{level} | {msg}", stacklevel=2)

    @staticmethod
    def warn(msg: str) -> None:
        """输出警告日志"""
        level = "WARN".center(6)
        Logger.logger.warning(f"{level} | {msg}", stacklevel=2)


class PasswordHasher:
    """密码哈希与校验工具类"""

    @staticmethod
    def hash(plain_password: str) -> str:
        """对明文密码进行加盐哈希"""
        # 生成随机盐
        salt = bcrypt.gensalt()
        # 计算哈希值
        hashed = bcrypt.hashpw(plain_password.encode(), salt)
        return hashed.decode()

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """校验明文密码与哈希密码是否一致"""
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


class JwtUtil:
    """JWT 令牌工具类"""

    @staticmethod
    def encode(payload: JwtPayload) -> str:
        """根据载荷生成 JWT 令牌"""
        return jwt.encode(
            payload.model_dump(),
            app_settings.jwt.secret_key,
            algorithm=app_settings.jwt.algorithm
        )

    @staticmethod
    def decode(token: str) -> JwtPayload:
        """解析并验证 JWT 令牌"""
        data = jwt.decode(
            token,
            app_settings.jwt.secret_key,
            algorithms=[app_settings.jwt.algorithm]
        )
        return JwtPayload(**data)

    @staticmethod
    def validate(token: str) -> JwtPayload:
        """验证 token 是否有效"""
        return JwtUtil.decode(token)


class ApiResponse:
    """统一 API 响应结构"""

    @staticmethod
    def _wrap(data=None, msg: str = '', code: int = 0):
        """内部统一返回格式包装"""
        return {"code": code, "msg": msg, "data": data}

    @staticmethod
    def success(data=None, msg: str = "操作成功", code: int = 200):
        """成功响应"""
        return ApiResponse._wrap(data, msg, code)

    @staticmethod
    def fail(msg: str = "操作失败", data=None, code: int = 400):
        """失败响应"""
        return ApiResponse._wrap(data, msg, code)


class DateTimeUtils:
    """时间工具类"""

    @staticmethod
    def now() -> float:
        """获取当前时间戳"""
        return datetime.now().timestamp()

    @staticmethod
    def expire() -> float:
        """计算过期时间戳"""
        return (datetime.now() + timedelta(hours=app_settings.jwt.expire_hours)).timestamp()


class CacheUtils:
    """Redis 缓存工具类"""

    # 类变量，保存单例 Redis 实例
    _redis_instance = None

    @classmethod
    def init_redis(cls) -> None:
        """初始化 Redis 连接，全局只执行一次"""
        if not cls._redis_instance:
            cls._redis_instance = redis.Redis(
                host=app_settings.cache.host,
                port=app_settings.cache.port,
                db=app_settings.cache.database,
                password=app_settings.cache.password
            )

    @classmethod
    def get_redis(cls) -> redis.Redis:
        """获取 Redis 单例实例"""
        if not cls._redis_instance:
            cls.init_redis()
        return cls._redis_instance  # type: ignore

    @classmethod
    def set(cls, key: str, value: str, ex: int = None) -> None:
        """写入缓存"""
        cls.get_redis().set(key, value, ex=ex)

    @classmethod
    def get(cls, key: str) -> str | None:
        """读取缓存"""
        return cls.get_redis().get(key)  # type: ignore

    @classmethod
    def delete(cls, key: str) -> None:
        """删除指定缓存"""
        cls.get_redis().delete(key)


# 项目启动时初始化 Redis
CacheUtils.init_redis()
