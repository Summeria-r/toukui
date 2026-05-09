from typing import Dict, Optional
from datetime import datetime, timedelta
import pandas as pd
from app.models.zptable import ZpTable
from app.models.userinfo import UserInfo
from tortoise.expressions import Q


async def get_community_posts(page: int = 1, page_size: int = 10, status: Optional[str] = None, search: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    """获取车友圈帖子列表"""
    # 构建查询
    query = ZpTable.all()
    
    # 按状态筛选
    if status:
        query = query.filter(Q(status=status))
    
    # 按关键词搜索
    if search:
        query = query.filter(Q(zptitle__icontains=search))
    
    # 按时间范围筛选
    if start_date:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Q(zpsj__gte=start_date_obj))
    
    if end_date:
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
        query = query.filter(Q(zpsj__lte=end_date_obj))
    
    # 获取总数
    total = await query.count()
    
    # 分页
    total_pages = (total + page_size - 1) // page_size
    start = (page - 1) * page_size
    posts = await query.offset(start).limit(page_size).order_by("-zpsj").all()
    
    # 转换为字典格式并获取用户名
    post_list = []
    for post in posts:
        # 查询用户信息
        user = await UserInfo.filter(id=post.userid).first()
        user_name = user.account if user else "未知用户"
        
        post_dict = {
            "id": post.id,
            "user_id": post.userid,
            "user": user_name,
            "title": post.zptitle,
            "content": post.zpcontent,
            "images": ["image.jpg"] if post.zpimg else [], 
            "status": post.status,
            "create_time": post.zpsj.strftime("%Y-%m-%d %H:%M:%S"),
            "review_time": post.audit_time.strftime("%Y-%m-%d %H:%M:%S") if post.audit_time else None,
            "reject_reason": post.reject_reason,
            "likes": post.zpdz,
            "comments": post.pl
        }
        post_list.append(post_dict)
    
    return {
        "posts": post_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

async def approve_post(post_id: int) -> Dict:
    """批准帖子"""
    post = await ZpTable.filter(Q(id=post_id)).first()
    if post:
        post.status = "approved"
        post.audit_time = datetime.now()
        await post.save()
        return {"success": True, "message": "帖子已批准"}
    return {"success": False, "message": "帖子不存在"}

async def reject_post(post_id: int, reject_reason: str) -> Dict:
    """拒绝帖子"""
    post = await ZpTable.filter(Q(id=post_id)).first()
    if post:
        post.status = "rejected"
        post.reject_reason = reject_reason
        post.audit_time = datetime.now()
        await post.save()
        return {"success": True, "message": "帖子已拒绝"}
    return {"success": False, "message": "帖子不存在"}

async def get_post_detail(post_id: int) -> Optional[Dict]:
    """获取帖子详情"""
    post = await ZpTable.filter(Q(id=post_id)).first()
    if post:
        # 查询用户信息
        user = await UserInfo.filter(id=post.userid).first()
        user_name = user.account if user else "未知用户"
        
        # 处理图片
        images = []
        if post.zpimg:
            import base64
            # 将二进制图片数据转换为base64编码
            img_base64 = base64.b64encode(post.zpimg).decode('utf-8')
            # 构建data URL
            img_url = f"data:image/jpeg;base64,{img_base64}"
            images.append(img_url)
        
        post_dict = {
            "id": post.id,
            "user_id": post.userid,
            "user": user_name,
            "title": post.zptitle,
            "content": post.zpcontent,
            "images": images,
            "status": post.status,
            "create_time": post.zpsj.strftime("%Y-%m-%d %H:%M:%S"),
            "review_time": post.audit_time.strftime("%Y-%m-%d %H:%M:%S") if post.audit_time else None,
            "reject_reason": post.reject_reason,
            "likes": post.zpdz,
            "comments": post.pl
        }
        return post_dict
    return None

async def export_community_posts() -> bytes:
    """导出帖子到Excel"""
    # 查询所有帖子
    posts = await ZpTable.all().order_by("-zpsj").all()
    
    # 转换为字典列表
    post_list = []
    for post in posts:
        # 查询用户信息
        user = await UserInfo.filter(id=post.userid).first()
        user_name = user.account if user else "未知用户"
        
        post_dict = {
            "ID": post.id,
            "发布用户": user_name,
            "标题": post.zptitle,
            "内容": post.zpcontent,
            "发布时间": post.zpsj.strftime("%Y-%m-%d %H:%M:%S"),
            "审核状态": "待审核" if post.status == "pending" else "已通过" if post.status == "approved" else "已拒绝",
            "审核时间": post.audit_time.strftime("%Y-%m-%d %H:%M:%S") if post.audit_time else "-",
            "拒绝理由": post.reject_reason or "-",
            "点赞数": post.zpdz,
            "评论数": post.pl
        }
        post_list.append(post_dict)
    
    # 创建DataFrame
    df = pd.DataFrame(post_list)
    
    # 创建Excel文件
    output = pd.ExcelWriter("community_posts.xlsx", engine="openpyxl")
    df.to_excel(output, index=False, sheet_name="车友圈帖子")
    output.close()
    
    # 读取Excel文件内容
    with open("community_posts.xlsx", "rb") as f:
        content = f.read()
    
    return content