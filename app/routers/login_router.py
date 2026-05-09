from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from config import DATAEASE_DASHBOARD_URL

from app.exceptions import InvalidParameterException, PasswordErrorException, UserNotExistsException
from app.security import delete_user_session, save_user_session
from app.services.login_services import login_user
templates = Jinja2Templates(directory="templates")
login_router = APIRouter()



@login_router.get("/")
async def login(request: Request):
    """登录页面"""
    return templates.TemplateResponse("index.html", {"request": request})


@login_router.post("/login")
async def login(
    request: Request,
    account: str = Form(...),
    password: str = Form(...),
):
    """登录 处理表单提交"""
    try:
        # 调用服务层完成登录校验
        user = await login_user(account, password)
        # 保存用户会话
        await save_user_session(request, user)

        # 登录成功：跳转数据可视化平台
        # 这里用 RedirectResponse 跳转，因为 POST 请求后要重定向到 GET 接口
        return RedirectResponse(url="http://192.168.199.129:8100/#/de-link/34Oz42xw", status_code=302)
        

    except InvalidParameterException as e:
        # 参数异常（账号/密码为空）
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": e.detail}
        )
    except UserNotExistsException as e:
        # 用户不存在（账号错误）
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": e.detail}
        )
    except PasswordErrorException as e:
        # 密码错误
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": e.detail}
        )
    except Exception as e:
        # 兜底异常（未知错误）
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "登录失败，请检查账号密码"}
        )
    
#退出登录
@login_router.get("/logout")
async def logout(request: Request):
    """退出登录"""
    try:
        # 删除用户会话
        await delete_user_session(request)
        # 退出成功，重定向到登录页
        return RedirectResponse(url="/", status_code=302)
    except Exception as e:
        # 处理退出失败的情况，比如会话不存在
        return RedirectResponse(url="/?error=退出失败，请重试", status_code=302)