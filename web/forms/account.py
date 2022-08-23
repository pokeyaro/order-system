import random

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_redis import get_redis_connection

from web import models
from utils.const import Role
from utils.encrypt import md5
from utils.message import send_sms


def check_phone(this):
    role = this.get('role')
    mobile = this['mobile']
    if not role:
        return mobile, None
    if role == Role.ADMIN:
        user_obj = models.Administrator.objects.filter(active=1, mobile=mobile).first()
    else:
        user_obj = models.Customer.objects.filter(active=1, mobile=mobile).first()
    if not user_obj:
        raise ValidationError("手机号不存在")
    return mobile, user_obj


class LoginForm(forms.Form):
    """
    <select class="form-select" name="role">
        <option value="2">客户</option>
        <option value="1">管理员</option>
    </select>
    """
    role = forms.ChoiceField(
        required=True,
        choices=(("2", "客户"), ("1", "管理员")),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="角色"
    )
    # <input type="text" class="form-control" id="username" placeholder="username" name="username">
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder": "username"}),
        label="用户名"
    )
    # <input type="password" class="form-control" id="password" placeholder="password" name="password">
    password = forms.CharField(
        required=True,
        min_length=5,
        max_length=16,
        validators=[RegexValidator(r'^\w+$', '密码格式错误'), ],  # 支持正则表达式格式校验
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder": "password"},
                                   render_value=True),
        label="密码"
    )

    # 支持字段的钩子函数验证
    def clean_username(self):
        user = self.cleaned_data['username']
        if len(user) < 4:
            raise ValidationError("用户名格式错误")
        return user

    def clean_password(self):
        return md5(self.cleaned_data['password'])

    def clean(self):
        if self.cleaned_data.get('username') is None or self.cleaned_data.get('password') is None:
            raise ValidationError("输入不合法")

    def _post_clean(self):
        pass


class SmsLoginForm(forms.Form):
    role = forms.ChoiceField(
        required=True,
        choices=(("2", "客户"), ("1", "管理员")),
        label="角色"
    )
    mobile = forms.CharField(
        required=True,
        label="手机号",
        validators=[RegexValidator(r'1[3-8]\d{9}', "手机号格式错误"), ]
    )
    code = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^\d{4}$', '验证码格式错误'), ],
        label="短信验证码"
    )

    def clean_mobile(self):
        # 1.验证手机号是否存在
        mobile, user_obj = check_phone(self.cleaned_data)
        if user_obj:
            self.cleaned_data.update({
                "username": user_obj.username,
                "userid": user_obj.id
            })
        return mobile

    def clean_code(self):
        # 短信验证码 + redis中获取验证码 => 验证
        mobile = self.cleaned_data.get("mobile")
        code = self.cleaned_data['code']
        if not mobile:
            return code

        conn = get_redis_connection("default")
        cache_code = conn.get(mobile)
        if not cache_code:
            raise ValidationError("短信验证码未发送或已失效")

        if code != cache_code.decode("utf-8"):
            raise ValidationError("短信验证码错误")

        return code


class MobileForm(forms.Form):
    role = forms.ChoiceField(
        required=True,
        choices=(("2", "客户"), ("1", "管理员")),
        label="角色"
    )
    mobile = forms.CharField(
        label="手机号",
        required=True,
        validators=[RegexValidator(r'1[3-8]\d{9}', "手机号格式错误"), ]
    )

    def clean_mobile(self):
        # 1.验证手机号是否存在
        mobile, _ = check_phone(self.cleaned_data)

        # 2.发送短信 + 生成验证码
        sms_code = str(random.randint(1000, 9999))
        is_success = send_sms(mobile, sms_code)
        if not is_success:
            raise ValidationError("发送失败，请稍后重试")

        # 3.将手机号和验证码保存（以便于下次校验） redis -> timeout
        try:
            conn = get_redis_connection("default")
            conn.set(mobile, sms_code, ex=60)
        except Exception as e:
            print("错误信息：" + str(e))
            raise ValidationError("手机号缓存信息保存失败")

        self.cleaned_data['code'] = sms_code
        return mobile
