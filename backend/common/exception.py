from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from common.utils import ApiResponse, Logger
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from redis.exceptions import ConnectionError as redis_ConnectionError


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

    # FastAPI 表单/文件/请求参数校验异常
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        err = exc.errors()[0]
        loc = " -> ".join(str(p) for p in err["loc"])
        raw_msg = err["msg"]

        tip = f"[{loc}] {raw_msg}"
        return JSONResponse(ApiResponse.fail(msg=tip))

    # Pydantic 模型校验异常
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        err = exc.errors()[0]
        loc = " -> ".join(str(p) for p in err["loc"])
        raw_msg = err["msg"]
        tip = f"[{loc}] {raw_msg}"
        return JSONResponse(ApiResponse.fail(msg=tip))

    @app.exception_handler(redis_ConnectionError)
    async def redis_connection_error_handler(request: Request, exc: ValidationError):
        Logger.error("Redis连接超时")
        return JSONResponse(ApiResponse.fail("内部错误"))
