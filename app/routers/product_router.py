from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form, Query, UploadFile, File
from typing import Optional
import os
from app.services.product_services import (
    get_product_list,
    create_product,
    update_product,
    delete_product,
    toggle_product_status,
    get_product_categories
)

templates = Jinja2Templates(directory="templates")
product_router = APIRouter()

# 确保上传目录存在
UPLOAD_DIR = "static/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@product_router.get("/product", response_class=HTMLResponse)
async def product_page(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    status: str = Query(None),
    category: str = Query(None),
    min_price: Optional[str] = Query(None),
    max_price: Optional[str] = Query(None),
    sort_by: str = Query(None),
    sort_order: str = Query(None)
):
    """商品管理页面"""
    # 处理价格参数
    min_price_float = float(min_price) if min_price else None
    max_price_float = float(max_price) if max_price else None
    
    result = await get_product_list(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        category=category,
        min_price=min_price_float,
        max_price=max_price_float,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    # 获取所有分类
    categories = await get_product_categories()
    
    return templates.TemplateResponse("product.html", {
        "request": request,
        "products": result["products"],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "total_pages": result["total_pages"],
        "search": search,
        "status": status,
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "categories": categories
    })

@product_router.post("/product/create")
async def create_product_api(
    name: str = Form(...),
    price: float = Form(...),
    total_count: int = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None)
):
    """创建商品"""
    # 处理图片上传
    image_url = None
    if image:
        # 生成唯一文件名
        filename = f"product_{os.urandom(8).hex()}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # 保存图片
        with open(file_path, "wb") as f:
            f.write(await image.read())
        
        # 构建图片URL
        image_url = f"/static/images/{filename}"
    
    result = await create_product(
        name=name,
        price=price,
        total_count=total_count,
        category=category,
        image=image_url
    )
    
    return JSONResponse(result)

@product_router.post("/product/update")
async def update_product_api(
    product_id: int = Form(...),
    name: str = Form(None),
    price: float = Form(None),
    total_count: Optional[int] = Form(None),
    sold_count: Optional[int] = Form(None),
    category: str = Form(None),
    status: str = Form(None),
    image: UploadFile = File(None)
):
    """更新商品"""
    # 构建更新参数
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if price is not None:
        update_data["price"] = price
    if total_count is not None:
        update_data["total_count"] = total_count
    if sold_count is not None:
        update_data["sold_count"] = sold_count
    if category is not None:
        update_data["category"] = category
    if status is not None:
        update_data["status"] = status
    
    # 处理图片上传
    if image and image.filename:
        # 生成唯一文件名
        filename = f"product_{os.urandom(8).hex()}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # 保存图片
        with open(file_path, "wb") as f:
            f.write(await image.read())
        
        # 构建图片URL
        update_data["image"] = f"/static/images/{filename}"
    
    result = await update_product(product_id, **update_data)
    return JSONResponse(result)

@product_router.post("/product/delete")
async def delete_product_api(product_id: int = Form(...)):
    """删除商品"""
    result = await delete_product(product_id)
    return JSONResponse(result)

@product_router.post("/product/toggle-status")
async def toggle_product_status_api(product_id: int = Form(...)):
    """切换商品状态"""
    result = await toggle_product_status(product_id)
    return JSONResponse(result)

@product_router.get("/product/categories")
async def get_categories_api():
    """获取商品分类"""
    categories = await get_product_categories()
    return JSONResponse({"categories": categories})

@product_router.get("/product/detail")
async def get_product_detail_api(product_id: int = Query(...)):
    """获取商品详情"""
    from app.models.product import Product
    from tortoise.expressions import Q
    
    product = await Product.filter(Q(id=product_id)).first()
    if not product:
        return JSONResponse({"success": False, "message": "商品不存在"})
    
    # 计算库存
    total_count = product.total_count or 0
    sold_count = product.sold_count or 0
    stock = total_count - sold_count
    
    return JSONResponse({
        "success": True,
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "total_count": total_count,
            "sold_count": sold_count,
            "stock": stock,
            "category": product.category,
            "image": product.image,
            "status": product.status
        }
    })