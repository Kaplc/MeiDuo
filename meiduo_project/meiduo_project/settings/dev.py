"""
Django settings for meiduo_project project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 追加BASE_DIR路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--_1f%o0k*2&z)$!r*yz*k_rf_5!i&q-o*03$s&0we0%h6ugls7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'pdd42.bolinkang.cn',
    'localhost',
    'www.meiduo.site',
    '611a78647w.oicp.vip',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_crontab',  # 定时任务

    # 使用追加的BASE_DIR注册user子应用

    'users',  # 用户模块
    'contents',  # 首页模块
    'verifications',  # 认证模块
    'oauth',  # QQ登录模块
    'areas',  # 省市区查询模块
    'goods',  # 商品信息模块
    'haystack',  # 全文检索
    'orders',  # 订单
    'payment',  # 支付
    'rest_framework',  # DRF
    'corsheaders',  # 跨域解决
    'meiduo_admin',  # 美多后台
]

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',  # 跨域解决
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_project.urls'

# --------------------------------------------------------------
# 配置模板引擎
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 补充Jinja2模板引擎环境
            'environment': 'meiduo_project.utils.jinja2_env.jinja2_environment',

        },
    },

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_project.wsgi.application'

# --------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# 配置mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库用户密码
        'NAME': 'meiduo',  # 数据库名字

    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------------------
# 配置redis

CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        # 采用10号库
        "LOCATION": "redis://127.0.0.1:6379/10",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {  # verify_code
        "BACKEND": "django_redis.cache.RedisCache",
        # 采用11号库
        "LOCATION": "redis://127.0.0.1:6379/11",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "celery": {  # celery
        "BACKEND": "django_redis.cache.RedisCache",
        # 采用12号库
        "LOCATION": "redis://127.0.0.1:6379/12",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 用户浏览记录
        "BACKEND": "django_redis.cache.RedisCache",
        # 采用13号库
        "LOCATION": "redis://127.0.0.1:6379/13",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 购物车
        "BACKEND": "django_redis.cache.RedisCache",
        # 采用14号库
        "LOCATION": "redis://127.0.0.1:6379/14",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# --------------------------------------------------------------
# 配置工程日志

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器

    # 日志信息显示的格式
    'formatters': {  # 日志信息显示的格式
        'verbose': {  # 详细日记格式
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {  # 简单日记格式
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },

    # 对日志进行过滤
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # 日志处理方法
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'DEBUG',  # 输出级别INFO
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,  # 每个日记文件的大小(字节)
            'backupCount': 100,  # 日记文件的数量, 满了自动创建
            'formatter': 'verbose'
        },
    },

    # 日志器
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# 重新定义迁移的用户模型类
# 原: 在django.conf.global_settings 内的 AUTH_USER_MODEL = 'auth.User'
# AUTH_USER_MODEL = '应用名.模型类名'
AUTH_USER_MODEL = 'users.User'

# ---------全局session过期时间----------
SESSION_COOKIE_AGE = 259200

# --------------------------指定自定义用户认证后端--------------------------- #
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBacken']

# --------------------------定义LoginRequiredMixin重定向地址--------------------------- #
LOGIN_URL = '/login.html/'

# --------------------------QQ开发者应用配置--------------------------- #
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

# --------------------------配置邮件服务器--------------------------- #
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
EMAIL_HOST = 'smtp.163.com'  # 发邮件主机
EMAIL_PORT = 25  # 发邮件端口
EMAIL_HOST_USER = 'zzy18475754696@163.com'  # 授权的邮箱
EMAIL_HOST_PASSWORD = 'FKBBCDGDNFYFUPPK'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '美多商城<zzy18475754696@163.com>'  # 发件人抬头

# --------------------------邮箱验证链接--------------------------- #
EMAIL_VERIFY_URL = 'http:///pdd42.bolinkang.cn:8081/emails/verification/'

# --------------------------fdfs配置参数--------------------------- #
# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = 'meiduo_project.utils.fastdfs.fdfs_storage.FastDFSStorage'
# FastDFS相关参数
FDFS_BASE_URL = 'http://192.168.43.14122122/'
# FDFS_BASE_URL = 'http://image.meiduo.site:8888/'

# --------------------------haystack--------------------------- #
# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        # 'URL': 'https://611a78647w.oicp.vip/',
        'URL': 'http://192.168.136.128:9200/',  # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo_mall',  # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# 设置每页返回数据条数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5

# --------------------------支付宝配置--------------------------- #
ALIPAY_APPID = '2021000122603082'
ALIPAY_DEBUG = True
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = 'http://pdd42.bolinkang.cn:8081/payment/status/'

# --------------------------定时任务--------------------------- #
CRONJOBS = [
    # 每1分钟生成一次首页静态文件
    ('*/1 * * * *', 'contents.crons.generate_static_index_html'),

]
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# -------------------跨域设置---------------
# CORS
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',

)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# ---------------------DRF------------------- #
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    # 过期认证时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 指定重写jwt返回
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'meiduo_project.apps.meiduo_admin.utils.jwt_response_payload_handler',
}
