from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from .models import UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


# 用户收藏
class UserFavSerializer(serializers.ModelSerializer):
    # 不提交用户，而是自动判断当前登录用户，所以用此字段
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=UserFav.objects.all(),
        #         fields=('user', 'goods'),
        #         message="已经收藏"
        #     )
        # ]

        fields = ("user", "goods", "id")

