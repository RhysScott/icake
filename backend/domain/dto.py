from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class JwtPayload(BaseDTO):
    """JWT 载荷模型"""
    user_id: int    # 用户ID
    iat: float      # 签发时间戳
    exp: float      # 过期时间戳

class ImageModel(BaseDTO):
    id: int
    index: int|None
    type: int
    path: str
    create_time: datetime|None
    update_time: datetime|None   

from pydantic import BaseModel
from datetime import datetime

class NoticeModel(BaseDTO):
    id: int
    title: str
    content: str
    status: int
    index: int | None
    create_time: datetime
    update_time: datetime
