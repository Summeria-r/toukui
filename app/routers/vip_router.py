from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from datetime import date
from app.services.vip_services import (
    get_vip_list, 
    update_vip_status, 
    delete_vip
)
from app.models.userinfo import UserInfo

vip_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@vip_router.get("/vip", response_class=HTMLResponse)
async def vip_page(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    end_date_min: Optional[str] = Query(None),
    end_date_max: Optional[str] = Query(None)
):
    """会员管理页面"""
    result = await get_vip_list(
        page=page,
        page_size=page_size,
        user_id=user_id,
        status=status,
        end_date_min=end_date_min,
        end_date_max=end_date_max
    )
    
    return templates.TemplateResponse("vip.html", {
        "request": request,
        "vips": result["vips"],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "total_pages": result["total_pages"],
        "user_id": user_id,
        "status": status,
        "end_date_min": end_date_min,
        "end_date_max": end_date_max
    })

@vip_router.get("/vip/export")
async def export_vip_excel(
    user_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    end_date_min: Optional[str] = Query(None),
    end_date_max: Optional[str] = Query(None)
):
    """导出会员列表为Excel"""
    from fastapi.responses import StreamingResponse
    import io
    import pandas as pd
    
    # 获取所有会员数据
    result = await get_vip_list(
        page=1,
        page_size=10000,  # 导出所有数据
        user_id=user_id,
        status=status,
        end_date_min=end_date_min,
        end_date_max=end_date_max
    )
    
    vips = result["vips"]
    
    # 转换为DataFrame
    df = pd.DataFrame(vips)
    
    # 重命名列
    df.rename(columns={
        "id": "ID",
        "user_id": "用户ID",
        "status": "会员状态",
        "start_date": "开始日期",
        "end_date": "结束日期"
    }, inplace=True)
    
    # 创建Excel文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='会员列表')
    output.seek(0)
    
    # 返回文件
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=会员列表.xlsx"}
    )

@vip_router.post("/vip/update-status")
async def update_vip_status_api(
    vip_id: int = Form(...),
    status: str = Form(...)
):
    """更新会员状态"""
    result = await update_vip_status(vip_id, status)
    return JSONResponse(result)

@vip_router.post("/vip/delete")
async def delete_vip_api(
    vip_id: int = Form(...)
):
    """删除会员"""
    result = await delete_vip(vip_id)
    return JSONResponse(result)