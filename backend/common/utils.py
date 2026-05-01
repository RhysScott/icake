import bcrypt
import jwt
from domain.dto import JwtPayload
from common.settings import app_settings
from datetime import datetime, timedelta
import redis
import logging
import os
import re
import pathlib
import redis



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

    @staticmethod
    def page(
        list=None,
        total: int = 0,
        page_num: int = 1,
        page_size: int = 10,
        msg: str = "操作成功",
        code: int = 200
    ):
        """
        标准分页响应
        :param list: 数据列表
        :param total: 总记录数
        :param page_num: 当前页码
        :param page_size: 每页条数
        """
        data = {
            "list": list or [],
            "total": total,           # 总条数
            "page_num": page_num,       # 当前页
            "page_size": page_size,     # 每页条数
            "pages": (total + page_size - 1) // page_size  # 总页数
        }
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


import json
import redis
from typing import Any
from common.settings import app_settings


class CacheUtils:
    """Redis 缓存工具（内置 JSON 序列化）"""
    _redis: redis.Redis | None = None

    @classmethod
    def init(cls) -> None:
        """项目启动时初始化一次连接"""
        if not cls._redis:
            cls._redis = redis.Redis(
                host=app_settings.cache.host,
                port=app_settings.cache.port,
                db=app_settings.cache.database,
                password=app_settings.cache.password,
                decode_responses=True,
                socket_timeout=0.5,
                socket_connect_timeout=0.5
            )

    @classmethod
    def client(cls) -> redis.Redis:
        """获取 Redis 客户端"""
        return cls._redis  # type: ignore

    @classmethod
    def set(cls, key: str, value: Any, ex: int = None) -> None:
        """写入缓存"""
        try:
            json_str = json.dumps(value, ensure_ascii=False, default=str)
            cls.client().set(key, json_str, ex=ex)
        except Exception:
            pass

    @classmethod
    def get(cls, key: str) -> Any:
        """读取缓存"""
        try:
            data = cls.client().get(key)  # type: ignore
            return json.loads(data) if data else None # type: ignore
        except Exception:
            return None


    @classmethod
    def delete(cls, key: str) -> None:
        """删除指定 key"""
        try:
            cls.client().delete(key)
        except Exception:
            pass

    @classmethod
    def mget(cls, keys: list[str]) -> list[Any | None]:
        """批量获取缓存"""
        if not keys:
            return []
        try:
            values = cls.client().mget(keys)  # type: ignore
            return [json.loads(v) if v else None for v in values] #type: ignore
        except Exception:
            return [None] * len(keys)

    @classmethod
    def delete_by_pattern(cls, pattern: str) -> int:
        """按通配符批量删除"""
        try:
            keys = cls.client().keys(pattern)  # type: ignore
            return cls.client().delete(*keys) if keys else 0  # type: ignore
        except Exception:
            return 0
# 启动时初始化
CacheUtils.init()


class PathUtils:
    @staticmethod
    def is_url(path: str) -> bool:
        """判断是否为 URL 链接"""
        if not path:
            return False
        return re.match(r'^https?://', path.strip()) is not None

    @staticmethod
    def is_file_path(path: str) -> bool:
        """判断是否为本地文件路径"""
        if not path:
            return False
        return not PathUtils.is_url(path)

    @staticmethod
    def get_path(path: str):
        if PathUtils.is_url(path):
            return path
        return (pathlib.Path(app_settings.upload.EXPOSED_BASE_DIR) / pathlib.Path(path)).as_posix()
