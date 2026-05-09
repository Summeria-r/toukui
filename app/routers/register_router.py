from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.services.register_services import register_user
from app.exceptions import InvalidParameterException, UserAlreadyExistsException
from config import TEMPLATES_DIR

register_router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@register_router.post("/do_register")
async def register(
    request: Request,
    account: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """注册 处理表单提交"""
    try:
        # 调用服务层完成注册，只传参数，不做任何逻辑
        await register_user(account, password, confirm_password)
        # 注册成功，跳转到登录页，带成功提示
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "success": "注册成功！请登录", "show_register": False}
        )
    except InvalidParameterException as e:
        # 参数错误（手机号格式/密码长度），返回注册页并提示
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": e.detail, "show_register": True}
        )
    except UserAlreadyExistsException as e:
        # 账号/手机号重复，返回注册页并提示
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": e.detail, "show_register": True}
        )
    except Exception as e:
        # # 兜底异常
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"注册失败原因: {str(e)}", "show_register": True}
        )