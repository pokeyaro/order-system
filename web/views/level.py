from django.shortcuts import render
from web import models


def level_list(request):
    queryset = models.Level.objects.filter(active=1)
    return render(request, 'level_list.html', {'queryset': queryset})


def level_add(request):
    return render(request, 'form.html')
