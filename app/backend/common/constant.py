class CacheKey:
    """缓存 Key 构造方法"""

    @staticmethod
    def sms_code(phone: str) -> str:
        return f"sms:code:{phone}"

    @staticmethod
    def user_info(user_id: int) -> str:
        return f"user:info:{user_id}"

    @staticmethod
    def user_token(user_id: int) -> str:
        return f"user:token:{user_id}"

    @staticmethod
    def reset_password_code(phone: str) -> str:
        return f"user:reset:pwd:code:{phone}"

    @staticmethod
    def token_blacklist(token: str) -> str:
        return f"token:blacklist:{token}"
