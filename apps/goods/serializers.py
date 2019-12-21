from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage, Banner


class CategorySerializer3(serializers.ModelSerializer):
    # 3级类别
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    # 2级类别
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    # model里外检字段的反查属性 sub_cat， 嵌套2级类别，不然看不到外键
    sub_cat = CategorySerializer2(many=True)  # 有很多个2类 所以many true

    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 外键关系，要用这种嵌套
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    # 嵌套上面的c瑞来啧，使外键完整，不然只有个id
    category = CategorySerializer()
    # 嵌套外键，字段名等于model里写的related_name="images"
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'


