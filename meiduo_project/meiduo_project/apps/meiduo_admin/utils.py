from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_response_payload_handler


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
