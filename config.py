# 配置文件 数据库地址、密钥、session密钥等

# config.py
from typing import Dict

# Tortoise-ORM 数据库配置
# TORTOISE_ORM: Dict = {
#     "connections": {
#         # 注意：等你把 MySQL 迁到 Docker，和 FastAPI、DataEase 一起用 Docker Compose 管理,这里用的是Docker Compose里MySQL服务的名字，不是localhost
#         "default": "mysql://root:123456@localhost:3306/toukuiinfo",
#     },
#     "apps": {
#         "models": {
#             "models": ["app.models", "aerich.models"],  # 修正为你的模型路径
#             "default_connection": "default"
#         }
#     },
#     "use_tz": False,
#     "timezone": "Asia/Shanghai",
#     "db_pool": {
#         "minsize": 1,
#         "maxsize": 10,
#         "idle_timeout": 300
#     }
# }
def get_tortoise_config() -> Dict:
    
    database_url = "mysql://root:iUHSZUHUNPxkZpqAqXFZQyXFxRyWRmYC@tramway.proxy.rlwy.net:54156/railway"
    return {
        "connections": {
            "default": database_url,
        },
        "apps": {
            "models": {
                 "models": ["app.models", "aerich.models"], 
                "default_connection": "default"
            }
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai",
        "db_pool": {
            "minsize": 1,
            "maxsize": 10,
            "idle_timeout": 300
        }
    }

# 会话加密密钥（生产环境请替换为随机长字符串，不要硬编码）
SECRET_KEY = "cyVAD3pKrudg83EkiUaF_-VYAYVDWu_wIk9PH1_lq_0"
# 会话过期时间（秒）
SESSION_MAX_AGE = 3600
# 模板目录
TEMPLATES_DIR = "templates"

#DataEase 数据可视化地址
DATAEASE_DASHBOARD_URL = "http://192.168.199.129:8100/#/de-link/340z42xw"