from django import forms
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from web import models
from utils.encrypt import md5
from utils.bootstrap import BootstrapForm


def customer_list(request):
    # 获取客户列表 queryset = [obj, obj, obj]
    # 主动跨表：将含有外键的做联表查询(一次性获取，查询效率提升，无需在template中再进行查询了)
    queryset = models.Customer.objects.filter(active=1).select_related('level', 'creator')
    context = {
        'queryset': queryset,
    }
    return render(request, 'customer_list.html', context)


class CustomerModelForm(BootstrapForm, forms.ModelForm):
    # exclude_filed_list = ['level']

    confirm_password = forms.CharField(
        label="重复密码",
        widget=forms.PasswordInput(render_value=True),
        help_text="请确保两次密码输入一致"
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # modelform想要显示关联数据：某个字段筛选时，重写过滤条件
        # 此处可能会用到request，进行条件筛选
        self.fields['level'].queryset = models.Level.objects.filter(active=1)
        for name, field in self.fields.items():
            field.widget.attrs['style'] = 'width: 220px'

    class Meta:
        model = models.Customer
        fields = ['username', 'mobile', 'password', 'confirm_password', 'level']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            # 'level': forms.RadioSelect(attrs={'class': 'form-redio'})
        }

    def clean_password(self):
        # 避免入库为明文
        password = self.cleaned_data['password']
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password', ''))
        if password != confirm_password:
            raise ValidationError('密码不一致')
        return confirm_password


def customer_add(request):
    if request.method == "GET":
        form = CustomerModelForm(request)
        return render(request, 'form3.html', {'form': form})

    # 校验数据
    form = CustomerModelForm(request, data=request.POST)
    if not form.is_valid():
        return render(request, 'form3.html', {'form': form})

    # 保存入库
    form.instance.creator_id = request.login_user.id
    form.save()

    return redirect(reverse('customer_list'))
