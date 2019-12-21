from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import SmsSerializer, UserRegSerializer
from utils.yunpian import YunPian
from fishshop.settings import APIKEY
from .models import VerifyCode


User = get_user_model()


# 自定义用户登录认证，配合drf_jwt
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 注册-，点击获取验证码接口
class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        随机生成4位数的验证码用来发送
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    # 重写CreateModelMixin 里的 create 方法，并在其中加入验证码发送
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                "mobile": sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)


# 注册，用户密码验证码
class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    注册用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写这个方法，可以让create 拿到user对象
    def perform_create(self, serializer):
        return serializer.save()

