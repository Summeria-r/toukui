from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

templates = Jinja2Templates(directory="templates")
video_router = APIRouter()

@video_router.get("/video",response_class=HTMLResponse)
async def video_page(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})