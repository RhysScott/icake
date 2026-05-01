from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class BaseVO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserLoginRequest(BaseVO):
    """用户登录请求参数"""
    phone: str = Field(..., description="手机号")
    password: str = Field(..., description="密码")


class UserRegisterRequest(BaseVO):
    """用户注册请求参数"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    password: str = Field(..., min_length=6, description="密码")
    nickname: Optional[str] = Field(None, description="昵称")


class UserUpdateRequest(BaseVO):
    """用户信息修改请求参数"""
    id: int
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[int] = None
    birthday: Optional[str] = None
    bio: Optional[str] = None


class UserPasswordResetRequest(BaseVO):
    """用户重置密码请求"""
    phone: str = Field(..., description="手机号")
    code: str = Field(..., description="验证码")
    password: str = Field(..., min_length=6, description="新密码")

class UserInfoResponse(BaseVO):
    """用户基础信息响应"""
    id: int
    phone: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[int] = None
    birthday: Optional[datetime] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    is_deleted: bool


class UserLoginResponse(BaseVO):
    """用户登录响应"""
    token: str
    user: UserInfoResponse


class ImageVO(BaseVO):
    id: int
    index: int|None
    type: int
    path: str
    create_time: datetime|None
    update_time: datetime|None   

class NoticeVO(BaseVO):
    id: int
    title: str
    content: str
    status: int
    index: int | None
    create_time: datetime|None
    update_time: datetime|None
