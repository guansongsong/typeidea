"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# from ..blog.admin import custom_site  # mmp
from custom_site import custom_site
from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView
)
from config.views import LinkListView
from comment.views import CommentView
from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
import xadmin
from .autocomplete import CategoryAutocompelete, TagAutocomplete
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from blog.apis import PostViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view



router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')



urlpatterns = [
    url(r'^rss/$', LatestPostFeed(), name='rss'),
    url(r'^sitemap.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^author/(?P<owner_id>\d+)$', AuthorView.as_view(), name='author'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),

    # url(r'^super_admin/', admin.site.urls, name='super-admin'),
    # url(r'^admin/', custom_site.urls, name='admin'),
    url(r'^admin/', xadmin.site.urls, ),

    url(r'^category-autocomplete/$', CategoryAutocompelete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),


    url(r'^api/', include(router.urls,)),


    url(r'api/docs/', include_docs_urls(title='typeidea apis')),     # drf自带的接口文档
    url(r"^docs/$", get_swagger_view(title="tyepidea apis")),        # swagger接口文档

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

