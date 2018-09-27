import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品价格过滤
    """
    pricemin = django_filters.NumberFilter(name='shop_price',lookup_expr='gte')
    #最小价格 大于等于
    pricemax = django_filters.NumberFilter(name='shop_price',lookup_expr='lte')
    #最大价格，小于等于
    name = django_filters.CharFilter(name='name',lookup_expr='icontains')
    #忽略大小写，查询name字段

    class Meta:
        model = Goods
        fields = ['pricemin','pricemax','name']