from django.shortcuts import render


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    # 1.接收并获取数据
    print(request.POST)
    # 2.校验
    return render(request, "login.html")


def sms_login(request):
    return render(request, "sms_login.html")
