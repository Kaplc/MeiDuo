from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical, users, goods, skus

app_name = 'meiduo_admin'

urlpatterns = [
    # 使用jwt认证后端
    re_path(r'meiduo_admin/authorizations/$', obtain_jwt_token),
    # ---------------------数据统计------------------- #
    # 用户总数
    re_path(r'meiduo_admin/statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    # 日注册用户
    re_path(r'meiduo_admin/statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    # 日活跃用户
    re_path(r'meiduo_admin/statistical/day_active/$', statistical.UserActiveCountView.as_view()),
    # 日下单用户
    re_path(r'meiduo_admin/statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    # 月活跃用户
    re_path(r'meiduo_admin/statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    # 日分类商品访问量
    re_path(r'meiduo_admin/statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    # --------------------用户---------------------- #
    # 查询，添加用户
    re_path(r'meiduo_admin/users/$', users.UserView.as_view()),
    # ---------------------商品管理--------------------- #
    # spu规格simple
    re_path(r'meiduo_admin/goods/simple/$', goods.SpecsView.as_view({'get': 'simple'})),
    # sku简单信息
    re_path(r'meiduo_admin/skus/simple/$', skus.ImageView.as_view({'get': 'simple'})),
    # categories
    re_path(r'meiduo_admin/skus/categories/$', skus.CategoriesView.as_view({'get': 'list'})),
    # 修改specs
    re_path(r'meiduo_admin/goods/(?P<pk>\d+)/specs/$', goods.SPUSpecView.as_view()),
    # brand
    re_path(r'meiduo_admin/goods/brands/simple/$', goods.BrandsSimpleView.as_view()),

]
# -------------------自动生成路由----------------------- #
# spu规格
router = DefaultRouter()
router.register('meiduo_admin/goods/specs', goods.SpecsView, basename='specs')
urlpatterns += router.urls
# SKU图片
router = DefaultRouter()
router.register('meiduo_admin/skus/images', skus.ImageView, basename='images')
urlpatterns += router.urls
# SKU
router = DefaultRouter()
router.register('meiduo_admin/skus', skus.SKUView, basename='skus')
urlpatterns += router.urls
# SPU
router = DefaultRouter()
router.register('meiduo_admin/goods', goods.SPUView, basename='spus')
urlpatterns += router.urls
