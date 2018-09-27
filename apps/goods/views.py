from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .models import Goods
from .serializers import GoodsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    '''
    分页配置，每页多少条数据
    '''
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewSet(viewsets.ModelViewSet):
    '''
    商品列表
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFilter