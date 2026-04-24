from pydantic import BaseModel

class JwtPayload(BaseModel):
    """JWT 载荷模型"""
    user_id: int    # 用户ID
    iat: float      # 签发时间戳
    exp: float      # 过期时间戳
