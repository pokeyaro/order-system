from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from web import models
from django import forms


class LevelModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'
            field.widget.attrs['style'] = 'width: 800px'

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
