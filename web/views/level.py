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
