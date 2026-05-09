from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form, Query
from app.services.community_services import get_community_posts, approve_post, reject_post, get_post_detail, export_community_posts

templates = Jinja2Templates(directory="templates")
community_router = APIRouter()

@community_router.get("/community",response_class=HTMLResponse)
async def community_page(
    request: Request, 
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    search: str = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None)):

    """车友圈管理页面"""
    result = await get_community_posts(page=page, page_size=page_size, status=status, search=search, start_date=start_date, end_date=end_date)
    return templates.TemplateResponse("community.html", {
        "request": request,
        "posts": result["posts"],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "total_pages": result["total_pages"],
        "status": status,
        "search": search,
        "start_date": start_date,
        "end_date": end_date
    })


@community_router.post("/community/approve")
async def approve_community_post(post_id: int = Form(...)):
    """审批车友圈帖子"""
    result = await approve_post(post_id)
    return result

@community_router.post("/community/reject")
async def reject_community_post(post_id: int = Form(...), reject_reason: str = Form(...)):
    """拒绝车友圈帖子"""
    result = await reject_post(post_id, reject_reason)
    return result

@community_router.get("/community/detail")
async def get_community_post_detail(post_id: int = Query(...)):
    """获取车友圈帖子详情"""
    post = await get_post_detail(post_id)
    return post

@community_router.get("/community/export")
async def export_community_posts_excel():
    """导出社友圈帖子"""
    content = await export_community_posts()
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=community_posts.xlsx"
        }
    )