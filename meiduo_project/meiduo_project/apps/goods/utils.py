from collections import OrderedDict

from goods.models import GoodsChannel


def get_breadcrumb(category):
    """
    查询面包屑导航
    :param category: 商品类别
    :return: 字典
    """
    # 三级->二级->一级
    breadcrumb = {
        'cat1': '',
        'cat2': '',
        'cat3': '',
    }

    if category.parent is None:
        # 没有父类别->一级标题
        breadcrumb['cat1'] = category
    elif category.subs.count() == 0:
        # 没有子类别->三级标题
        breadcrumb['cat3'] = category
        cat2 = category.parent
        breadcrumb['cat2'] = cat2
        breadcrumb['cat1'] = cat2.parent
    else:
        # 二级标题
        breadcrumb['cat1'] = category.parent
        breadcrumb['cat2'] = category

    return breadcrumb


def get_categories():
    """查询商品分类三级联动"""
    categories = OrderedDict()  # 有序字典
    # 商品组 <- 商品频道 -> 商品分类
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')  # 查询所有商品频道
    for channel in channels:
        # 每个频道的组
        group_id = channel.group_id
        # 判断group_id重复
        if group_id not in categories:
            # 构造组字典
            categories[group_id] = {
                'channels': [],
                'sub_cats': [],
            }

        # 获取频道id, 名字(类别), url并添加到channels列表
        category = channel.category  # channels获取category的表对象
        categories[group_id]['channels'].append({
            'id': channel.id,
            'name': category.name,
            'url': channel.url,
        })

        # 自连接查询二级类别
        for cat2 in category.subs.all():
            sub_cat3 = []
            # 自连接查询三级类别
            for cat3 in cat2.subs.all():
                sub_cat3.append({
                    'id': cat3.id,
                    'name': cat3.name,
                })

            categories[group_id]['sub_cats'].append({
                'id': cat2.id,
                'name': cat2.name,
                'sub_cats': sub_cat3,
            })

    return categories
