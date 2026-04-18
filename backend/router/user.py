from fastapi import APIRouter
from database import SessionFactory
from service import UserService
from domain.vo import (
    UserRegisterRequest, UserInfoResponse,
    UserPasswordResetRequest, UserUpdateRequest,
    UserLoginRequest
)

from utils import ApiResponse

router = APIRouter(prefix='/user')

@router.post("/register")
def register(req: UserRegisterRequest):
    with SessionFactory() as db: # 这里是一个数据库会话的工厂函数，不理解就算了，反正这么写可以拿到数据库的连接
        user = UserService.register(db, req)
        return ApiResponse.success(data=UserInfoResponse.model_validate(user).model_dump())

@router.post("/reset-password")
def reset_password(req: UserPasswordResetRequest):
    with SessionFactory() as db:
        UserService.reset_password(db, req)
        return ApiResponse.success(msg="密码重置成功")

@router.post("/update")
def update_info(req: UserUpdateRequest, user_id: int = 1):
    with SessionFactory() as db:
        user = UserService.update_info(db, user_id, req)
        return ApiResponse.success(data=UserInfoResponse.model_validate(user))

@router.post("/login")
def login(req: UserLoginRequest):
    with SessionFactory() as db:
        token, user = UserService.login(db, req)
        return ApiResponse.success(data={
            "token": token,
            "user": UserInfoResponse.model_validate(user)
        })
