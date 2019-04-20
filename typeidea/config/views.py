from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView
from blog.views import CommonViewMinxin
from . import models
# Create your views here.


class LinkListView(CommonViewMinxin, ListView):
    queryset = models.Link.objects.filter(status=models.Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'