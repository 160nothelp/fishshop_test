from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permission import IsOwnerOrReadOnly
from .models import UserFav, UserLeavingMessage, UserAddress


# 用户收藏
# DestroyModelMixin 删除用的，需要delete方法，并且可自动识别uri后面的/id
class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):

    # 只允许 登录用户删除他自己的藏品
    # 第一个是 登录验证， 第二个就是 表的owner验证，当前行是不是属于当前登陆的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 局部token验证， 和session认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 只允许get 当前登录用户的收藏信息
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


