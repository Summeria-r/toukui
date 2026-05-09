from tortoise import Model, fields

class VideoPlayback(Model):
    """视频播放表"""
    # 视频ID（主键、自增）
    id = fields.IntField(pk=True, index=True, description="视频ID")
    
    # 视频名称
    name = fields.CharField(max_length=255, description="视频名称")
    # 视频地址（可空）
    url = fields.CharField(max_length=500, null=True, description="视频地址")
    # 缩略图地址（可空）
    thumbnail = fields.CharField(max_length=500, null=True, description="缩略图地址")
    # 日期
    record_date = fields.DateField(description="日期")
    # 时间段
    time_segment = fields.CharField(max_length=50, description="时间段")
    # 时长
    duration = fields.CharField(max_length=20, description="时长")
    # 是否新视频（默认1，对应tinyint）
    is_new = fields.BooleanField(default=True, description="是否新视频")
    
    # 创建时间（自动记录当前时间）
    create_time = fields.DatetimeField(
        auto_now_add=True,
        description="创建时间"
    )
    # 更新时间（修改时自动更新）
    update_time = fields.DatetimeField(
        auto_now=True,
        description="更新时间"
    )

    class Meta:
        table = "video_playback"
        description = "视频回放表"