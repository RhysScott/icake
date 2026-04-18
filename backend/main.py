from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from utils import Logger
from router import register_router
from exception import register_exception_handlers

Logger.info("日志模块初始化完成")

# 创建 FastAPI 应用实例
app = FastAPI(title="小蛋糕 API", version="1.0")
Logger.info("FastAPI 应用实例创建完成")

# 注册跨域中间件，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许所有域名
    allow_credentials=True,    # 允许携带 Cookie
    allow_methods=["*"],       # 允许所有请求方法
    allow_headers=["*"],       # 允许所有请求头
)
Logger.info("CORS 跨域中间件注册完成")

# 统一注册所有路由
Logger.info("开始注册全局路由模块")
register_router(app)
Logger.info("全部路由模块注册完成")


if __name__ == "__main__":
    # 打印项目启动横幅
    with open('banner.txt', 'r', encoding='utf-8') as f:
        print(f.read())
        
    # 启动 Uvicorn 服务
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )
