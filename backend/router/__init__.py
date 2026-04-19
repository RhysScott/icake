from fastapi import FastAPI
from common.utils import Logger


def register_router(app: FastAPI):
    """
    统一注册所有路由到 FastAPI 应用实例
    - 采用延迟导入方式
    """
    # 宝宝们，Python的模块会在导入时加载，而且不管导入多少次，只会加载一次
    # 注册公共模块路由
    from .common_router import router as common_router
    app.include_router(common_router)
    Logger.info("公共路由模块注册完成")

    # 注册用户模块路由
    from .user import router as user_router
    app.include_router(user_router)
    Logger.info("用户路由模块注册完成")
