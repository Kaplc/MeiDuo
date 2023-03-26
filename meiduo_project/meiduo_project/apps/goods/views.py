import copy
import json
from django import http
from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views import View
from .contents import *
from goods.models import GoodsCategory, SKU, GoodsVisitCount
from meiduo_project.utils.response_code import RETCODE
from .utils import get_categories, get_breadcrumb
import logging

logger = logging.getLogger('django')


class GoodsCommentView(View):
    """订单商品评价信息"""

    def get(self, request, sku_id):
        """获取商品评价数据"""

        try:
            # 校验参数
            sku = SKU.objects.get(id=sku_id)
            # 构造评论列表
            comment_list = []
            # 查询评论
            order_goods = sku.ordergoods_set.all()
            for order_good in order_goods:
                comment_list.append({
                    'username': order_good.order.user.username,
                    'comment': order_good.comment,
                    'score': order_good.score
                })
            pass
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': 'sku_id错误'})

        # 构造json数据
        json_data ={
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'comment_list': comment_list
        }
        return http.JsonResponse(json_data)


class DetailVisitView(View):
    """统计商品访问量"""

    def post(self, request, category_id):
        """
        统计商品访问量
        :param request:
        :param category_id: 商品分类ID，第三级分类
        :return:JSON
        """
        # 校验参数
        try:
            category = GoodsCategory.objects.get(id=category_id)

        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('缺少必传参数')

        # 获取日期
        time = timezone.now()
        # 日期字符串
        time_str = '%d-%02d-%02d' % (time.year, time.month, time.day)
        # 转datetime类型的日期对象
        time_object = datetime.datetime.strptime(time_str, '%Y-%m-%d')
        # 查询今日该商品访问量, 没有则新建
        try:
            counts_data = category.goodsvisitcount_set.get(date=time_object)

        except Exception as e:
            logger.error(e)
            # 找不到记录就新建对象
            counts_data = GoodsVisitCount()

        try:
            counts_data.category = category
            counts_data.date = time_object
            counts_data.count += 1
            counts_data.save()

        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('服务器错误')

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class DetailView(View):
    """商品详情"""

    def get(self, request, sku_id):
        """展示商品详情页"""
        # 接收参数
        sku_id = sku_id
        # 校验参数, 获取sku信息
        try:
            sku = SKU.objects.get(id=sku_id)

        except Exception as e:
            logger.error(e)
            return render(request, '404.html')

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

        return render(request, 'detail.html', context)


class HotGoodsView(View):
    """热销排行"""

    def get(self, request, category_id):
        """展示热销排行"""
        # 查找商品sku
        try:
            # -sales销量降序, 切片取前两个
            skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[0:2]

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '热销排行查询失败'})
        # model_list转json数据
        skus_list = []
        for sku in skus:
            skus_list.append({
                'id': sku.id,
                'default_image_url': sku.default_image_url.url,
                'name': sku.name,
                'price': sku.price,
            })
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'hot_skus': skus_list
        })


class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """展示页面"""
        # 校验查询category_id
        try:
            category = GoodsCategory.objects.get(id=category_id)

        except Exception as e:
            logger.error(e)
            return http.HttpResponseNotFound('未找到数据')
        # 查询商品分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)
        # 获取sort排序方式
        sort = request.GET.get('sort')
        # 判断页面排序方式
        if sort == 'price':
            # 价格降序, 默认升序
            sort_field = 'price'
        elif sort == 'hot':
            # 热度降序
            sort_field = '-sales'
        else:
            # 其他情况
            sort = 'default'  # 重置排序参数
            sort_field = 'create_time'
        try:
            # 查询sku商品预览(条件: 商品类别, 是否上架)
            skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by(sort_field)

        except Exception as e:
            logger.error(e)
            return http.HttpResponseNotFound('找不到商品信息')

        # sku分页
        paginator = Paginator(skus, CONTENT_QUANTITY)  # Paginator(分页内容, 每页数量)
        # 获取每页数据
        try:
            sku_page = paginator.page(page_num)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseNotFound('找不到该页商品信息')
        # 总页数
        total_page = paginator.num_pages
        # jinja渲染内容
        context = {
            'categories': categories,  # 商品分类列表
            'breadcrumb': breadcrumb,  # 面包屑导航
            'sku_page': sku_page,  # 每页数据
            'sort': sort,  # 排序规则
            'page_num': page_num,  # 当前所在页
            'total_page': total_page,  # 总页数
            'category_id': category_id,  # 当前商品类别id
            'category': category,  # 当前商品类别
        }

        return render(request, 'list.html', context)
