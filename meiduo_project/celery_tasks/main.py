# celery启动文件
from celery import Celery

# 创建celery实例
# 'MeiDuo': 别名
celery_app = Celery('MeiDuo')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])  # 不能漏列表
