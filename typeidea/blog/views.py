from django.shortcuts import render, HttpResponse, redirect
from . import models
from config.models import SideBar
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from comment.models import Comment
from comment.forms import CommentForm
from datetime import date
from django.core.cache import cache

# Create your views here.


# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#     if tag_id:
#         posts_list, tag = models.Post.get_by_tag(tag_id)
#     elif category_id:
#         posts_list, category = models.Post.get_by_category(category_id)
#     else:
#         posts_list = models.Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': posts_list,
#         'sidebars': SideBar.get_all()
#     }
#     context.update(models.Category.get_navs())
#     return render(request, 'blog/list1.html', context=context)


# def post_detail(request, post_id=None):
#     try:
#         post = models.Post.objects.get(id=post_id)
#     except models.Post.DoesNotExist:
#         post = None
#     content = {
#         'post': post,
#         'sidebars': SideBar.get_all()
#     }
#     return render(request, 'blog/detail.html', context=content)


# class PostDetailView(DetailView):
#     model = models.Post
#     template_name = 'blog/detail.html'
#     # context_object_name = 'aaa'


# class PostListView(ListView):
#     queryset = models.Post.latest_posts()
#     paginate_by = 1  # 每页一条数据
#     context_object_name = 'post_list'  # 默认是object_list
#     template_name = 'blog/list1.html'


class CommonViewMinxin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'sidebars': SideBar.get_all(),
            }
        )
        context.update(models.Category.get_navs())
        return context


class IndexView(CommonViewMinxin, ListView):
    queryset = models.Post.latest_posts()
    paginate_by = 2
    context_object_name = 'post_list'
    template_name = 'blog/list1.html'


class SearchView(IndexView):
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'keyword': self.request.GET.get('keyword', '')
    #     })
    #     return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(models.Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(models.Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMinxin, DetailView):
    queryset = models.Post.latest_posts()
    # model = models.Post
    template_name = 'blog/detail.html'

    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

        # models.Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1, uv=F('uv')+1)
        #
        # #  查看orm对应的sql语句
        # from django.db import connection
        # print(connection.queries)
        # return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s' % (uid, self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)
        if increase_pv and increase_uv:
            models.Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,
                                                                 uv=F('uv')+1)
        elif increase_pv:
            models.Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            models.Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)