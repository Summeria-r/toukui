from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.sessions import SessionMiddleware
from config import SECRET_KEY, SESSION_MAX_AGE, get_tortoise_config

from app.routers.login_router import login_router
from app.routers.register_router import register_router
from app.routers.dashboard_router import dashboard_router
from app.routers.user_router import user_router
from app.routers.vip_router import vip_router
from app.routers.community_router import community_router
from app.routers.product_router import product_router
from app.routers.video_router import video_router
app = FastAPI()

# 1.静态资源挂载
app.mount("/static",StaticFiles(directory="static"),name="static")
app.mount("/templates",StaticFiles(directory="templates"),name="templates")
# 2.模板引擎配置
templates = Jinja2Templates(directory="templates")

# 3.注册Tortoise-ORM
register_tortoise(
    app,
    config=get_tortoise_config(),
    generate_schemas=False,
    add_exception_handlers=True
)

# 4.挂载Session会话中间件
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=SESSION_MAX_AGE
)
# 4.注册路由
app.include_router(register_router)
app.include_router(login_router)
app.include_router(dashboard_router)
app.include_router(user_router)
app.include_router(vip_router)
app.include_router(community_router)
app.include_router(product_router)
app.include_router(video_router)


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)