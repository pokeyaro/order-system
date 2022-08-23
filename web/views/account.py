from django.shortcuts import render, redirect
from django.http import JsonResponse
from web import models
from utils.encrypt import md5
from utils.message import send_sms
from django_redis import get_redis_connection
# 引入Form组件 / 表单验证
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random


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
        return self.cleaned_data['password']

    def clean(self):
        if self.cleaned_data.get('username') is None or self.cleaned_data.get('password') is None:
            raise ValidationError("输入不合法")

    def _post_clean(self):
        pass


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    # 1.接收并获取数据（数据格式或是否为空的验证 - Form组件 & ModelForm组件））
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        # 验证失败
        return render(request, "login.html", {"form": form})

    # 验证通过后，无需在request.POST中获取，可以在form.cleaned_data中获取
    # 如：{'role': '2', 'username': 'root', 'password': 'root'}
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password")
    password = md5(password)
    role = form.cleaned_data.get("role")

    # 2.去数据库校验
    mapping = {"1": "admin", "2": "customer"}
    if role not in mapping:
        # 错误信息，展示在特定字段旁
        form.add_error("role", "角色不存在")
        return render(request, "login.html", {"form": form})
    if role == "1":
        user_obj = models.Administrator.objects.filter(active=1, username=username, password=password).first()
    else:
        user_obj = models.Customer.objects.filter(active=1, username=username, password=password).first()

    # 2-1.校验失败
    if not user_obj:
        form.add_error("username", "用户名或密码错误")
        return render(request, "login.html", {"form": form})

    # 2-2.校验成功
    # 用户信息写入session
    request.session['user_info'] = {"role": mapping[role], "name": user_obj.username, "id": user_obj.id}
    # 跳转进入项目后台
    return redirect("/home/")


class SmsLoginForm(forms.Form):
    role = forms.ChoiceField(
        required=True,
        choices=(("2", "客户"), ("1", "管理员")),
        label="角色"
    )
    mobile = forms.CharField(
        required=True,
        label="手机号"
    )
    code = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^\d+$', '验证码必须为数字'), ],
        label="短信验证码"
    )


def sms_login(request):
    if request.method == "GET":
        form = SmsLoginForm()
        return render(request, "sms_login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "sms_login.html", {"form": form})


class MobileForm(forms.Form):
    mobile = forms.CharField(label="手机号", required=True, validators=[RegexValidator(r'1[3-8]\d{9}', "手机号格式错误"), ])


class DataResponse(object):
    """ 统一的返回对象格式 """
    def __init__(self):
        self.status = False
        self.detail = None
        self.data = None

    @property
    def dict(self):
        return self.__dict__


def sms_send(request):
    """ 发送短信 """
    resp = DataResponse()

    # 1.校验手机号格式
    request.POST.get("mobile")
    form = MobileForm(data=request.POST)
    if not form.is_valid():
        # print(form.errors.as_json())
        resp.detail = form.errors
        return JsonResponse(resp.dict, json_dumps_params={"ensure_ascii": False})

    # 2.发送短信 + 生成验证码
    mobile = form.cleaned_data['mobile']
    sms_code = str(random.randint(1000, 9999))
    is_success = send_sms(mobile, sms_code)
    if not is_success:
        resp.detail = {"mobile": ["发送失败，请稍后重试"]}
        return JsonResponse(resp.dict, json_dumps_params={"ensure_ascii": False})

    # 3.将手机号和验证码保存（以便于下次校验） redis -> timeout
    try:
        conn = get_redis_connection("default")
        conn.set(mobile, sms_code, ex=60)
    except Exception as e:
        print("错误信息：" + str(e))
        resp.detail = {"mobile": ["手机号缓存信息保存失败"]}
        return JsonResponse(resp.dict, json_dumps_params={"ensure_ascii": False})

    # 4.成功的数据返回
    resp.status = True
    resp.data = {"mobile": mobile, "code": sms_code}
    return JsonResponse(resp.dict)
