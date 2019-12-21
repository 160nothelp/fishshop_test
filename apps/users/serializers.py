from rest_framework import serializers
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from fishshop.settings import REGEX_MOBILE
from .models import VerifyCode


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    # 验证mobile字段 函数名就是 validate 与字段名的拼接
    def validate_mobile(self, mobile):
        """
        y验证手机号
        :param attrs:
        :return:
        """
        # 手机是否被注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")

        # 手机合法性
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60秒")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    # 因为 userprofile 表里没有 code字段，所以要自己写一下,而且序列化的时候，不能展示(因为表里没有),所以设为只写
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 write_only=True,
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误',
                                 })
    # validators=[UniqueValidator：drf的验证器，唯一验证，判断用户是否已存在
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')],
                                     )
    # style可以让密码在drf的api页变成密文显示(有腿用？)，也是只读字段
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # def create(self, validated_data):
    #     # user为 当前设置的model的对象
    #     user = super(UserRegSerializer, self).create(validated_data)
    #     # 因为 User 继承Django内部类，内部类有set_password方法
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # initial_data['username'] 是表单获取的post数据
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError('验证码错误')

    # 全局验证方法重写
    def validate(self, attrs):
        # 前端不会提交mobile字段过来，但是后端库里还有这个字段，而且username也用的手机号，所以手动添加mobile字段
        attrs["mobile"] = attrs["username"]
        # 表里没有 code字段，code只是验证用的，所以验证完成后删掉，不需要提交到库
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')

