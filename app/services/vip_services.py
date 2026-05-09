from typing import Dict, List, Optional
from datetime import date, datetime
from tortoise.expressions import Q
from app.models.vipinfo import VipInfo
from app.models.userinfo import UserInfo

async def get_vip_list(
    page: int = 1, 
    page_size: int = 10, 
    user_id: Optional[int] = None, 
    status: Optional[str] = None, 
    end_date_min: Optional[str] = None, 
    end_date_max: Optional[str] = None
) -> Dict:
    """获取会员列表"""
    # 构建查询
    query = VipInfo.all()
    
    # 按用户ID筛选
    if user_id:
        query = query.filter(Q(user_id=user_id))
    
    # 按状态筛选
    if status:
        query = query.filter(Q(status=status))
    
    # 按到期时间筛选
    if end_date_min:
        query = query.filter(Q(end_date__gte=end_date_min))
    if end_date_max:
        query = query.filter(Q(end_date__lte=end_date_max))
    
    # 计算总数
    total = await query.count()
    
    # 排序并获取数据
    vips = await query.order_by("-id").offset((page - 1) * page_size).limit(page_size).values("id", "user_id_id", "status", "start_date", "end_date")
    print("vips里的第一条数据：", vips[0])
    
    # 转换为字典列表
    vip_list = []
    for vip in vips:
        vip_dict = {
            "id": vip.get("id"),
            "user_id": vip.get("user_id_id"),
            "status": vip.get("status"),
            "start_date": vip.get("start_date").isoformat() if vip.get("start_date") else "",
            "end_date": vip.get("end_date").isoformat() if vip.get("end_date") else ""
        }
        vip_list.append(vip_dict)
    print("vip_list里的第一条数据：", vip_list[0])
    return {
        "vips": vip_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

# async def get_vip_by_id(vip_id: int) -> Optional[Dict]:
#     """根据ID获取会员信息"""
#     vip = await VipInfo.filter(Q(id=vip_id)).values("id", "user_id", "start_date", "end_date", "status").first()
#     return vip

# async def create_or_update_vip(
#     user_id: int, 
#     start_date: date, 
#     end_date: date, 
#     status: str = "active"
# ) -> Dict:
#     """创建或更新会员信息"""
#     # 检查用户是否存在
#     user = await UserInfo.filter(Q(id=user_id)).values("id").first()
#     if not user:
#         return {"success": False, "message": "用户不存在"}
    
#     # 检查是否已有会员记录
#     existing_vip = await VipInfo.filter(Q(user_id=user_id)).values().first()
    
#     if existing_vip:
#         # 更新现有记录
#         await VipInfo.filter(Q(id=existing_vip.get("id"))).update(
#             start_date=start_date,
#             end_date=end_date,
#             status=status
#         )
#         # 获取更新后的记录
#         vip = await VipInfo.filter(Q(id=existing_vip.get("id"))).values().first()
#     else:
#         # 创建新记录
#         # 注意：这里我们不能直接使用create后获取对象，因为会导致AttributeError
#         # 所以我们先创建，然后再通过查询获取
#         await VipInfo.create(
#             user_id=user_id,
#             start_date=start_date,
#             end_date=end_date,
#             status=status
#         )
#         # 获取创建的记录
#         vip = await VipInfo.filter(Q(user_id=user_id)).values().first()
    
#     return {
#         "success": True,
#         "message": "会员信息更新成功",
#         "vip": {
#             "id": vip.get("id", ""),
#             "user_id": vip.get("user_id", ""),
#             "status": vip.get("status", ""),
#             "start_date": vip.get("start_date").isoformat() if vip.get("start_date") else "",
#             "end_date": vip.get("end_date").isoformat() if vip.get("end_date") else ""
#         }
#     }

async def update_vip_status(vip_id: int, status: str) -> Dict:
    """更新会员状态"""
    vip = await VipInfo.filter(Q(id=vip_id)).first()
    if not vip:
        return {"success": False, "message": "会员信息不存在"}
    
    await VipInfo.filter(Q(id=vip_id)).update(status=status)
    
    return {
        "success": True, "message": "会员状态更新成功",
        "status": status
    }

async def delete_vip(vip_id: int) -> Dict:
    """删除会员信息"""
    vip = await VipInfo.filter(Q(id=vip_id)).first()
    if not vip:
        return {"success": False, "message": "会员信息不存在"}
    
    await VipInfo.filter(Q(id=vip_id)).delete()
    
    return {"success": True, "message": "会员信息删除成功"}