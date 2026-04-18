from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime

class UserLoginRequest(BaseModel):
    """用户登录请求参数"""
    phone: str = Field(..., description="手机号")
    password: str = Field(..., description="密码")


class UserRegisterRequest(BaseModel):
    """用户注册请求参数"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    password: str = Field(..., min_length=6, description="密码")
    nickname: Optional[str] = Field(None, description="昵称")


class UserUpdateRequest(BaseModel):
    """用户信息修改请求参数"""
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[int] = None
    birthday: Optional[str] = None
    bio: Optional[str] = None

class UserPasswordResetRequest(BaseModel):
    """用户重置密码请求"""
    phone: str = Field(..., description="手机号")
    code: str = Field(..., description="验证码")
    password: str = Field(..., min_length=6, description="新密码")

class UserInfoResponse(BaseModel):
    """用户基础信息响应"""
    id: int
    phone: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    create_time: datetime

    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    """用户登录响应（token + 用户信息）"""
    token: str
    user: UserInfoResponse
