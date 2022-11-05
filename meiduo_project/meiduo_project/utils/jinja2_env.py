from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        # 重新定义static, url方法
        # 确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句

        # 调用static自动拼接静态文件目录的路径
        'static': staticfiles_storage.url,

        # url调用反向解析reverse
        'url': reverse,
    })
    return env
