from contextvars import ContextVar
from fastapi import HTTPException


_ctx_user_id: ContextVar[int | None] = ContextVar("user_id", default=None)

class RequestContext:
    @staticmethod
    def set_user_id(user_id: int | None):
        _ctx_user_id.set(user_id)

    @staticmethod
    def get_user_id() -> int:
        uid = _ctx_user_id.get()
        if uid is None:
            raise HTTPException(status_code=401, detail="请先登录")
        return uid

    @staticmethod
    def clear():
        _ctx_user_id.set(None)
