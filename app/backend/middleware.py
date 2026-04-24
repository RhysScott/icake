from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from common.utils import JwtUtil, Logger
from common.context import RequestContext
import json

WHITE_LIST = [
    "/user/login",
    "/user/register",
    "/docs",
    "/redoc",
    "/openapi.json"
]

class PreauthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path
        Logger.info(f"[鉴权中间件] 请求路径: {path}")

        # 放行 OPTIONS
        if request.method == "OPTIONS":
            Logger.info("[鉴权中间件] 已放行 OPTIONS 预检请求")
            return await call_next(request)

        # 白名单放行
        if any(path.startswith(p) for p in WHITE_LIST):
            Logger.info(f"[鉴权中间件] 白名单放行: {path}")
            return await call_next(request)

        # 获取 token
        auth = request.headers.get("Authorization", "")
        token = auth.replace("Bearer ", "").strip()

        if not token:
            return Response(
                content=json.dumps({"code": 401, "msg": "请先登录"}),
                status_code=401,
                media_type="application/json"
            )

        # 校验 token
        try:
            payload = JwtUtil.decode(token)
            user_id = payload.user_id
            Logger.info(f"[鉴权中间件] TOKEN校验成功 → user_id: {user_id}")
            RequestContext.set_user_id(user_id)

        except Exception as e:
            Logger.error(f"[鉴权中间件] TOKEN无效: {str(e)}")
            return Response(
                content=json.dumps({"code": 401, "msg": "登录已过期"}),
                status_code=401,
                media_type="application/json"
            )

        # 执行接口
        response = await call_next(request)

        # 重置上下文
        RequestContext.clear()

        return response


def register_middlewares(app: FastAPI):
    app.add_middleware(PreauthMiddleware)
