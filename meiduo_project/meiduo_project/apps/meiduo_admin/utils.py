import copy

from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from goods.models import SKU
from goods.utils import get_categories, get_breadcrumb


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义字段返回"""
    return {
        'token': token,
        'user': user.id,
        'username': user.username
    }


class PageNum(PageNumberPagination):
    """分页器"""
    page_size = 5  # 后端指定每页显示数量
    page_size_query_param = 'pagesize'  # 获取前端参数pagesize
    max_page_size = 10

    # 重写分页返回方法，按照指定的字段进行分页数据返回
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # 总数量
            'lists': data,  # 用户数据
            'page': self.page.number,  # 当前页数
            'pages': self.page.paginator.num_pages,  # 总页数
            'pagesize': self.page_size  # 后端指定的页容量

        })


def detail_page(sku_id):
    """展示商品详情页"""
    # 接收参数
    sku_id = sku_id
    # 校验参数, 获取sku信息
    try:
        sku = SKU.objects.get(id=sku_id)

    except Exception as e:

        return None
    # 获取商品分类
    categories = get_categories()
    # 获取面包屑导航
    breadcrumb = get_breadcrumb(sku.category)
    # 获取当前sku的规格选项
    sku_options_list = []
    sku_specs = sku.specs.all()
    for sku_spec in sku_specs:
        # 把当前选项存入选项列表
        sku_options_list.append(sku_spec.option.id)

    # 构建sku_id-选项字典
    skuid_option_dict = {}
    # 当前sku->spu->有关所有sku, 可以查询到所有选项与sku的组合
    skus = sku.spu.sku_set.all()
    for each_sku in skus:
        esku_specs = each_sku.specs.all()
        esku_specs_list = []
        for esku_spec in esku_specs:
            esku_specs_list.append(esku_spec.option.id)
        skuid_option_dict[tuple(esku_specs_list)] = each_sku.id

    # 获取当前商品的所有规格种类
    goods_specs = sku.spu.specs.all()
    for index, spec in enumerate(goods_specs):
        # 深拷贝复制当前选项的列表
        key = copy.deepcopy(sku_options_list)
        # 获取当前规格种类的所有选项
        # 动态将选项集合写入spec_options对象
        spec.spec_options = spec.options.all()
        # 遍历每个选项并标记当前所选定的选项
        for spec_option in spec.spec_options:
            # 动态创建对象初始化选项都都标记为False
            spec_option.curr_option = False
            # 遍历当前选择的选项id列表
            for sku_options_list_id in sku_options_list:
                # 判断当前选项id是否为所选的, 并标记
                if sku_options_list_id == spec_option.id:
                    spec_option.curr_option = True

            # 把规格1的选项id重新赋值
            key[index] = spec_option.id
            # 查找规格2不变时规格1变化的skuid并赋值
            spec_option.sku_id = skuid_option_dict.get(tuple(key))

    # jinja2渲染内容
    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs,
        'sku_options': sku_options_list,
    }

    response = render(None, 'detail.html', context)
    return response
