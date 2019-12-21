from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    '''
    分页配置，每页多少条数据
    '''
    # 默认单页大小
    page_size = 12
    # 自定义 页面大小 key名
    page_size_query_param = 'page_size'
    # 自定义的 页数 key名
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 公开页不需要token验证
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    ordering_fields = ('sold_num', 'shop_price')
    search_fields = ('name', 'goods_brief', 'goods_desc')


class CategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    list:
        商品分类
    """
    # mixins.RetrieveModelMixin: 用来接收uri跟参的mixin，就不需要在router或者url path 上配置了
    # 用法，在uri后面 跟/id/  记住是id号
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
