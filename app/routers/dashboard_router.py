from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Request, Response
import httpx

templates = Jinja2Templates(directory="templates")
dashboard_router = APIRouter()


# 数据大屏页面（导航栏+iframe）
@dashboard_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# @dashboard_router.get("/dashboard-proxy")
# async def dashboard(request: Request):
#     # 用 httpx 直接请求 DataEase 的大屏页面
#     async with httpx.AsyncClient() as client:
#         resp = await client.get("http://192.168.199.129:8100/#/de-link/340z42xw")
#         # 直接把 DataEase 返回的 HTML 作为响应发给浏览器
#         return HTMLResponse(resp.text)


# @dashboard_router.get("/dashboard")
# async def dashboard(request: Request):
#     async with httpx.AsyncClient() as client:
#         resp = await client.get("http://192.168.199.129:8101/de-link/340z42xw")
#         return templates.TemplateResponse("dashboard.html", {
#             "request": request,
#             "dashboard_content": resp.text
#         })