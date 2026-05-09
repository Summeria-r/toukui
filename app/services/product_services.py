from typing import List, Dict, Optional
from app.models.product import Product
from tortoise.expressions import Q
import pandas as pd
from io import BytesIO

async def get_product_list(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None
) -> Dict:
    """获取商品列表"""
    # 构建查询
    query = Product.all()
    
    # 搜索条件
    if search:
        # 尝试将搜索关键词转换为整数，用于ID搜索
        try:
            search_id = int(search)
            # 用 Q 对象实现 AND/OR 查询
            query = query.filter(
                Q(id=search_id) | Q(name__contains=search)
            )
        except ValueError:
            # 如果不是数字，则只搜索商品名称
            query = query.filter(
                Q(name__contains=search)
            )
    
    # 状态筛选
    if status:
        query = query.filter(Q(status=status))
    
    # 分类筛选
    if category:
        query = query.filter(Q(category=category))
    
    # 价格区间筛选
    if min_price is not None:
        query = query.filter(Q(price__gte=min_price))
    if max_price is not None:
        query = query.filter(Q(price__lte=max_price))
    
    # 排序
    if sort_by:
        order_expr = f"{'-' if sort_order == 'desc' else ''}{sort_by}"
        query = query.order_by(order_expr)
    else:
        # 默认按ID排序
        query = query.order_by("-id")
    
    # 计算总数
    total = await query.count()
    
    # 分页
    products = await query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 转换为字典列表
    product_list = []
    for product in products:
        # 计算库存
        total_count = product.total_count or 0
        sold_count = product.sold_count or 0
        stock = total_count - sold_count
        
        # 自动标记售罄
        if stock <= 0:
            if product.status != "sold_out":
                product.status = "sold_out"
                await product.save()
        
        product_dict = {
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
        product_list.append(product_dict)
    
    return {
        "products": product_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

async def create_product(name: str, price: float, total_count: int, category: str, image: Optional[str] = None) -> Dict:
    """新增商品"""
    # 计算库存
    stock = total_count
    
    # 确定状态
    status = "on_sale" if stock > 0 else "sold_out"
    
    # 创建商品
    product = await Product.create(
        name=name,
        price=price,
        total_count=total_count,
        sold_count=0,
        category=category,
        image=image,
        status=status
    )
    
    return {
        "success": True,
        "message": "商品创建成功",
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "total_count": product.total_count,
            "sold_count": product.sold_count,
            "stock": stock,
            "category": product.category,
            "image": product.image,
            "status": product.status
        }
    }

async def update_product(product_id: int, **kwargs) -> Dict:
    """更新商品"""
    product = await Product.filter(Q(id=product_id)).first()
    if not product:
        return {"success": False, "message": "商品不存在"}
    
    # 更新字段
    for key, value in kwargs.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    # 重新计算库存和状态
    total_count = product.total_count or 0
    sold_count = product.sold_count or 0
    stock = total_count - sold_count
    if stock <= 0:
        product.status = "sold_out"
    else:
        product.status = "on_sale"
    
    await product.save()
    
    return {
        "success": True,
        "message": "商品更新成功",
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "total_count": product.total_count,
            "sold_count": product.sold_count,
            "stock": stock,
            "category": product.category,
            "image": product.image,
            "status": product.status
        }
    }

async def delete_product(product_id: int) -> Dict:
    """删除商品"""
    product = await Product.filter(Q(id=product_id)).first()
    if not product:
        return {"success": False, "message": "商品不存在"}
    
    await product.delete()
    
    return {"success": True, "message": "商品删除成功"}

async def toggle_product_status(product_id: int) -> Dict:
    """切换商品状态（上架/下架）"""
    product = await Product.filter(Q(id=product_id)).first()
    if not product:
        return {"success": False, "message": "商品不存在"}
    
    # 计算库存
    stock = product.total_count - product.sold_count if product.total_count and product.sold_count else 0
    
    # 切换状态
    if product.status == "on_sale":
        product.status = "off_sale"
    elif product.status == "off_sale":
        product.status = "on_sale" if stock > 0 else "sold_out"
    
    await product.save()
    
    return {
        "success": True,
        "message": "商品状态更新成功",
        "status": product.status
    }

async def get_product_categories() -> List[str]:
    """获取所有商品分类"""
    categories = await Product.all().distinct().values_list("category", flat=True)
    return [cat for cat in categories if cat]