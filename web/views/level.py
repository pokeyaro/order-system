from django import forms
from django.urls import reverse
from django.shortcuts import render, redirect

from web import models
from utils.bootstrap import BootstrapForm


class LevelModelForm(BootstrapForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['style'] = 'width: 500px'

    class Meta:
        model = models.Level
        fields = ['title', 'percent']


def level_list(request):
    queryset = models.Level.objects.filter(active=1)
    return render(request, 'level_list.html', {'queryset': queryset})


def level_add(request):
    if request.method == "GET":
        form = LevelModelForm()
        return render(request, 'form.html', {'form': form})
    form = LevelModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'form.html', {'form': form})

    form.save()
    return redirect(reverse('level_list'))


def level_edit(request, pk):
    # 编辑功能（显示当前默认值）
    level_obj = models.Level.objects.filter(id=pk, active=1).first()
    if request.method == "GET":
        form = LevelModelForm(instance=level_obj)
        return render(request, 'form.html', {'form': form})
    # 获取数据 + 校验
    form = LevelModelForm(data=request.POST, instance=level_obj)
    if not form.is_valid():
        return render(request, 'form.html', {'form': form})
    # 根据id将用户提交的数据进行更新
    form.save()
    return redirect(reverse('level_list'))


def level_delete(request, pk):
    # 逻辑删除
    models.Level.objects.filter(id=pk).update(active=0)
    return redirect(reverse('level_list'))

