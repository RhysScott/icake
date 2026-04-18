from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSetting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,          # 不加载 .env 文件
        env_mode="strict",      # 禁用环境变量自动加载
        extra="forbid",         # 禁止多余字段（安全）
        case_sensitive=False,   # 不区分大小写
        validate_default=True,  # 校验默认值

    ) # type: ignore

# JWT 配置
class JwtSettings(BaseSetting):
    secret_key: str = "s8>f.;ys&3WwEMSU#Mwz4Y[hx-XnDTHmQTP"
    algorithm: str = "HS256"
    expire_hours: int = 2
    token_prefix: str = "Bearer "

# 数据库配置
class DatabaseSettings(BaseSetting):
    host: str = "noahmiller.icu"
    port: int = 3306
    username: str = "root"
    password: str = "kissme"
    database: str = "icake"
    dialect: str = "mysql"
    db_api: str = "pymysql"
    echo: bool = False

    @property
    def db_url(self) -> str:
        return f"{self.dialect}+{self.db_api}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

# Redis 缓存配置
class CacheSettings(BaseSetting):
    host: str = "localhost"
    port: int = 6379
    database: int = 0
    password: str | None = None

# 全局配置
class AppSettings(BaseSetting):
    jwt: JwtSettings = JwtSettings()
    db: DatabaseSettings = DatabaseSettings()
    cache: CacheSettings = CacheSettings()

# 全局单例
app_settings = AppSettings()
