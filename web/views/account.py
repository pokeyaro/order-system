from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from web import models
from utils.const import Role
from utils.response import BaseResponse
from web.forms.account import LoginForm, MobileForm, SmsLoginForm


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    # 1.接收并获取数据（数据格式或是否为空的验证 - Form组件 & ModelForm组件））
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        # 验证失败
        return render(request, "login.html", {"form": form})

    # 2.去数据库校验
    # 验证通过后，无需在request.POST中获取, 可以在form.cleaned_data中获取
    # 如: {'role': '2', 'username': 'root', 'password': 'root'}
    data_dict = form.cleaned_data
    role = data_dict.pop("role")
    if role == Role.ADMIN:
        user_obj = models.Administrator.objects.filter(active=1).filter(**data_dict).first()
    else:
        user_obj = models.Customer.objects.filter(active=1).filter(**data_dict).first()

    # 2-1.校验失败
    if not user_obj:
        form.add_error("username", "用户名或密码错误")
        return render(request, "login.html", {"form": form})

    # 2-2.校验成功, 用户信息写入session, 跳转进入项目后台
    mapping = {"1": "admin", "2": "customer"}
    request.session['user_info'] = {"role": mapping[role], "name": user_obj.username, "id": user_obj.id}

    return redirect(settings.LOGIN_HOME)


def sms_login(request):
    if request.method == "GET":
        form = SmsLoginForm()
        return render(request, "sms_login.html", {"form": form})

    resp = BaseResponse()
    # 1.手机格式校验 + 其他验证码校验
    form = SmsLoginForm(data=request.POST)
    if not form.is_valid():
        resp.detail = form.errors
        return JsonResponse(resp.dict, json_dumps_params={"ensure_ascii": False})

    # 2.用户信息写入session
    data_dict = form.cleaned_data
    role = data_dict['role']
    username = data_dict['username']
    userid = data_dict['userid']
    mapping = {"1": "admin", "2": "customer"}
    request.session['user_info'] = {"role": mapping[role], "name": username, "id": userid}

    resp.status = True
    resp.data = settings.LOGIN_HOME
    return JsonResponse(resp.dict)


def sms_send(request):
    """ 发送短信 """
    resp = BaseResponse()

    # 1.校验数据合法性
    request.POST.get("mobile")
    form = MobileForm(data=request.POST)
    if not form.is_valid():
        # print(form.errors.as_json())
        resp.detail = form.errors
        return JsonResponse(resp.dict, json_dumps_params={"ensure_ascii": False})

    # 2.成功的数据返回
    # 如: {'role': '1', 'mobile': '18888888888', 'code': '1581'}
    data_dict = form.cleaned_data
    data_dict.pop("role")
    resp.status = True
    resp.data = data_dict
    return JsonResponse(resp.dict)

