"""fishshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import xadmin
from fishshop.settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import GoodsListViewSet, CategoryViewset
from users.views import SmsCodeViewset, UserViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()

# 商品页
router.register(r'goods', GoodsListViewSet, base_name='goods')
# title商品分类
router.register(r'categorys', CategoryViewset, base_name='categorys')
# 验证码
router.register(r'codes', SmsCodeViewset, base_name='codes')
# 注册
router.register(r'users', UserViewset, base_name='users')

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # api页面用户管理
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # drf 的router
    url(r'^', include(router.urls)),
    # drf token
    # url(r'^api-token-auth/', views.obtain_auth_token)
    # jwt token
    url(r'^login/', obtain_jwt_token),

]
