from django.shortcuts import render, redirect
from web import models
from utils.encrypt import md5

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    # 1.接收并获取数据
    username = request.POST.get("username")
    password = request.POST.get("password")
    password = md5(password)
    role = request.POST.get("role")

    # 2.去数据库校验
    mapping = {"1": "admin", "2": "customer"}
    if role not in mapping:
        return render(request, "login.html", {"error": "角色不存在"})
    if role == "1":
        user_obj = models.Administrator.objects.filter(active=1, username=username, password=password).first()
    else:
        user_obj = models.Customer.objects.filter(active=1, username=username, password=password).first()

    # 2-1.校验失败
    if not user_obj:
        return render(request, "login.html", {"error": "用户名或密码错误"})

    # 2-2.校验成功
    # 用户信息写入session
    request.session['user_info'] = {"role": mapping[role], "name": user_obj.username, "id": user_obj.id}
    # 跳转进入项目后台
    return redirect("/home/")


def sms_login(request):
    return render(request, "sms_login.html")
