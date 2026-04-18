from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from common.utils import ApiResponse


# 业务异常
class BusinessException(Exception):
    """业务异常"""
    def __init__(self, msg: str = "操作失败", code: int = 400, data=None):
        self.msg = msg
        self.code = code
        self.data = data
        super().__init__(self.msg)


class TokenException(Exception):
    """Token认证异常"""
    def __init__(self, msg: str = "身份认证失败", code: int = 401, data=None):
        self.msg = msg
        self.code = code
        self.data = data
        super().__init__(self.msg)


# 统一注册异常处理器
def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        return JSONResponse(
            content=ApiResponse.fail(exc.msg, exc.data, exc.code),
            status_code=200
        )

    @app.exception_handler(TokenException)
    async def token_exception_handler(request: Request, exc: TokenException):
        return JSONResponse(
            content=ApiResponse.fail(exc.msg, exc.data, exc.code),
            status_code=401
        )
