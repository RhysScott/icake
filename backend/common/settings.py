from pydantic_settings import BaseSettings


# JWT 身份验证配置
class JwtSettings(BaseSettings):
    # 密钥，用于签名令牌
    secret_key: str = "s8>f.;ys&3WwEMSU#Mwz4Y[hx-XnDTHmQTP"
    # 加密算法
    algorithm: str = "HS256"
    # 令牌过期时间，单位小时
    expire_hours: int = 2
    # 请求头令牌前缀
    token_prefix: str = "Bearer "


# 数据库连接配置
class DatabaseSettings(BaseSettings):
    # 数据库地址
    host: str = "noahmiller.icu"
    # 端口
    port: int = 3306
    # 用户名
    username: str = "root"
    # 密码
    password: str = "kissme"
    # 数据库名
    database: str = "icake"
    # 数据库方言
    dialect: str = "mysql"
    # 数据库驱动
    db_api: str = "pymysql"
    # 是否打印 SQL 语句
    echo: bool = False

    @property
    def db_url(self):
        # 拼接数据库连接 URL
        url = f"{self.dialect}+{self.db_api}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        return url


# Redis 缓存配置
class CacheSettings(BaseSettings):
    # 服务地址
    host: str = "localhost"
    # 端口
    port: int = 6379
    # 数据库编号
    database: int = 0
    # 密码，没有则为空
    password: str | None = None


# 应用全局总配置
class AppSettings(BaseSettings):
    # JWT 配置
    jwt: JwtSettings = JwtSettings()
    # Redis 配置
    cache: CacheSettings = CacheSettings()
    # 数据库配置
    db: DatabaseSettings = DatabaseSettings()


# 创建全局配置单例
app_settings = AppSettings()
