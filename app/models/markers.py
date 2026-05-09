from tortoise import Model, fields

class Markers(Model):
    """心愿地点标记表"""
    # 标记ID（自增主键）
    id = fields.IntField(pk=True, index=True, description="标记ID（自增）")
    
    # 用户ID（varchar类型，不是int）
    userid = fields.CharField(max_length=50, description="用户ID")
    
    # 纬度 decimal(10,8)
    latitude = fields.DecimalField(max_digits=10, decimal_places=8, description="纬度")
    # 经度 decimal(11,8)
    longitude = fields.DecimalField(max_digits=11, decimal_places=8, description="经度")
    
    # 图标路径（可空）
    iconPath = fields.CharField(max_length=255, null=True, description="图标路径")
    # 图标宽度（可空）
    width = fields.IntField(null=True, description="图标宽度")
    # 图标高度（可空）
    height = fields.IntField(null=True, description="图标高度")
    
    # 地点名称
    localname = fields.CharField(max_length=255, description="地点名称")
    
    # 是否完成(0-未完成 1-已完成)，默认0
    isGone = fields.BooleanField(default=False, description="是否完成(0-未完成 1-已完成)")
    
    # 创建时间（自动记录）
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    # 更新时间（自动更新）
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "markers"
        description = "心愿地点标记表"