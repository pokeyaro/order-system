from django.shortcuts import render, redirect
from web import models
from utils.encrypt import md5

# 引入Form组件 / 表单验证
from django import forms


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
        widget=forms.Select(attrs={"class": "form-select"})
    )
    # <input type="text" class="form-control" id="username" placeholder="username" name="username">
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder": "username"})
    )
    # <input type="password" class="form-control" id="password" placeholder="password" name="password">
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder": "password"},
                                   render_value=True)
    )


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    # 1.接收并获取数据（数据格式或是否为空的验证 - Form组件 & ModelForm组件））
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        print("验证失败")
        return render(request, "login.html", {"form": form})
    print(form.cleaned_data)     # {'role': '2', 'username': 'root', 'password': 'root'}

    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password")
    password = md5(password)
    role = form.cleaned_data.get("role")

    # 2.去数据库校验
    mapping = {"1": "admin", "2": "customer"}
    if role not in mapping:
        return render(request, "login.html", {"form": form, "error": "角色不存在"})
    if role == "1":
        user_obj = models.Administrator.objects.filter(active=1, username=username, password=password).first()
    else:
        user_obj = models.Customer.objects.filter(active=1, username=username, password=password).first()

    # 2-1.校验失败
    if not user_obj:
        return render(request, "login.html", {"form": form, "error": "用户名或密码错误"})

    # 2-2.校验成功
    # 用户信息写入session
    request.session['user_info'] = {"role": mapping[role], "name": user_obj.username, "id": user_obj.id}
    # 跳转进入项目后台
    return redirect("/home/")


def sms_login(request):
    return render(request, "sms_login.html")
