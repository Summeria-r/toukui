from tortoise import Model, fields
from enum import Enum

class VipInfo(Model):
    """会员信息表"""
    id = fields.IntField(pk=True, description="主键ID")
    user_id = fields.ForeignKeyField(
        "models.UserInfo",
        related_name="vip_infos",
        on_delete=fields.CASCADE, 
        on_update=fields.NO_ACTION,
        source_field="id",  # 关联 UserInfo 的 id 字段
        db_column="user_id",  # 显式指定数据库列名
        description="用户ID"
    )
    start_date = fields.DateField(null=True, description="开始日期")
    end_date = fields.DateField(null=True, index=True, description="结束日期")
    status = fields.CharField(max_length=20, default="inactive")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "vipinfo"