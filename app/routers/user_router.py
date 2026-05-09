from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Query, Form
from app.services.user_services import get_user_list, export_users_to_excel, update_user, update_user_status

templates = Jinja2Templates(directory="templates")
user_router = APIRouter()

@user_router.get("/user",response_class=HTMLResponse)
async def user_page(
    request: Request,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页大小"),
    search: str = Query(None, description="搜索关键词"),
    status: str = Query(None, description="用户状态")
):
    # 获取用户列表
    result = await get_user_list(page, page_size, search, status)
    
    # 传递参数到模板
    context = {
        "request": request,
        "users": result["users"],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "total_pages": result["total_pages"],
        "search": search,
        "status": status
    }
    
    return templates.TemplateResponse("user.html", context)

@user_router.get("/user/export")
async def export_users():
    # 导出用户数据到Excel
    excel_data = await export_users_to_excel()
    
    # 返回Excel文件
    return StreamingResponse(
        excel_data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=users.xlsx"
        }
    )

@user_router.post("/user/update")
async def update_user_info(
    user_id: int = Form(...),
    account: str = Form(...),
    password: str = Form(None),
    status: str = Form(...)
):
    # 更新用户信息
    await update_user(user_id, account, password, status)
    
    # 重定向回用户管理页面
    return RedirectResponse(url="/user", status_code=302)

@user_router.post("/user/disable")
async def disable_user(
    user_id: int = Form(...)
):
    # 禁用用户
    await update_user_status(user_id, "1")
    
    # 返回成功信息
    return PlainTextResponse("User disabled successfully")