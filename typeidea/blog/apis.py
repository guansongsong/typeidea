from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from  django.urls import reverse
from .models import Post, Category, Tag
from .serializers import (
    PostSerializer, PostDetailSerializer,
    CategorySerializer, CatetoryDetailSerializer,)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        '''
        这里添加的内容swagger显示出来
        '''
        a = self.reverse_action('list')
        b = self.reverse_action('detail', args=[1])
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            return queryset.filter(category_id=category_id)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CatetoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)