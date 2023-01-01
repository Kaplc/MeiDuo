import os
from collections import OrderedDict

from django.conf import settings
from django.template import loader

from contents.models import ContentCategory
from goods.utils import get_categories


def generate_static_index_html():
    """生成静态html文件"""
    # 查询商品频道和分类
    categories = get_categories()
    # 查询首页广告数据
    contents = OrderedDict()
    for cat in ContentCategory.objects.all():
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
    # 定义上下文
    context = {
        'categories': categories,
        'contents': contents,
    }
    # 获取首页模板文件
    template = loader.get_template('index.html')
    # 渲染html字符串
    html_text = template.render(context)
    # 将指定文件写入指定目录, 命名 'index.html'
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)

