from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical, users, goods, skus, orders, permission, specs

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
    # -----------------goods------------------------- #
    # # spu规格
    # re_path(r'meiduo_admin/goods/specs/$', goods.SpecsView.as_view({'get': 'list'})),
    # 修改specs
    re_path(r'meiduo_admin/goods/(?P<pk>\d+)/specs/$', goods.SPUSpecView.as_view()),
    # brand
    re_path(r'meiduo_admin/goods/brands/simple/$', goods.BrandsSimpleView.as_view()),
    # categories
    # 一级
    re_path(r'meiduo_admin/goods/channel/categories/$', goods.CategoriesView.as_view({'get': 'list'})),
    # 二，三级
    re_path(r'meiduo_admin/goods/channel/categories/(?P<pk>\d+)/$', goods.CategoriesView.as_view({'get': 'list'})),

    # ---------------------skus--------------------- #
    # sku简单信息
    re_path(r'meiduo_admin/skus/simple/$', skus.ImageView.as_view({'get': 'simple'})),
    # categories
    re_path(r'meiduo_admin/skus/categories/$', skus.CategoriesView.as_view({'get': 'list'})),

    # ------------------order------------------------ #
    # 订单修改status
    re_path(r'meiduo_admin/orders/(?P<pk>\d+)/status/$', orders.OrdersView.as_view({'put': 'status'})),

    # --------------------permission---------------------- #
    # content_types
    re_path(r'meiduo_admin/permission/content_types/$', permission.PermissionView.as_view({'get': 'content_types'})),
    # simple
    re_path(r'meiduo_admin/permission/simple/$', permission.PermissionView.as_view({'get': 'content_types'})),

]
# -------------------自动生成路由----------------------- #

# SPU
router = DefaultRouter()
router.register('meiduo_admin/goods/specs', goods.SpecsView, basename='goods_specs')
urlpatterns += router.urls

# SPU
router = DefaultRouter()
router.register('meiduo_admin/goods', goods.SPUView, basename='spus')
urlpatterns += router.urls

# ------------------------------------------ #
# SKU图片
router = DefaultRouter()
router.register('meiduo_admin/skus/images', skus.ImageView, basename='images')
urlpatterns += router.urls

# SKU
router = DefaultRouter()
router.register('meiduo_admin/skus', skus.SKUView, basename='skus')
urlpatterns += router.urls

# ------------------------------------------ #
# orders
router = DefaultRouter()
router.register('meiduo_admin/orders', orders.OrdersView, basename='orders')
urlpatterns += router.urls

# ------------------------------------------ #
# permission/perms
router = DefaultRouter()
router.register('meiduo_admin/permission/perms', permission.PermissionView, basename='permission')
urlpatterns += router.urls

# permission/groups
router = DefaultRouter()
router.register('meiduo_admin/permission/groups', permission.GroupsView, basename='groups')
urlpatterns += router.urls

# permission/admins
router = DefaultRouter()
router.register('meiduo_admin/permission/admins', permission.AdminView, basename='admins')
urlpatterns += router.urls

# ------------------specs------------------------ #
# specs
router = DefaultRouter()
router.register('meiduo_admin/specs/options', specs.SpecsOptionsView, basename='specs')
urlpatterns += router.urls
