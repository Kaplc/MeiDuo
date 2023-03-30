# celery启动文件
from celery import Celery
import os

# celery使用django配置文件
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_project.settings.dev'

# 创建celery实例
# 'MeiDuo': 别名
celery_app = Celery('MeiDuo')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(
    ['celery_tasks.sms', 'celery_tasks.send_email', 'celery_tasks.test', 'celery_tasks.generate_static'])  # 不能漏列表
