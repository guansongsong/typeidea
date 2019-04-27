from django.contrib import admin
from . import models
from django.utils.html import format_html
from django.urls import reverse
from .adminforms import PostAdminForm
from custom_site import custom_site
from base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
import xadmin


# class PostInline(admin.TabularInline):
class PostInline:
    model = models.Post
    # fields = ('title', 'desc')
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 1


@xadmin.sites.register(models.Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'create_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # inlines = (PostInline,)


@xadmin.sites.register(models.Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')


# class CategoryOwnerFilter(admin.SimpleListFilter):
#     title = '分类过滤器'
#     parameter_name = 'owner_category'
#
#     def lookups(self, request, model_admin):
#         return models.Category.objects.filter(owner=request.user).values_list('id', 'name')
#
#     def queryset(self, request, queryset):
#         category_id = self.value()
#         if category_id:
#             return queryset.filter(category_id=self.value())
#         return queryset


class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, admin_view, field_path):
        super().__init__(field, request, params, model, admin_view, field_path)
        self.lookup_choices = models.Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(models.Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = (
        'title', 'category', 'status',
        'create_time', 'owner', 'operator', 'pv', 'uv'
    )
    list_display_links = []
    # list_filter = [CategoryOwnerFilter, ]
    list_filter = ['title']
    search_fields = ['title', 'category__name']
    filter_horizontal = ('tag',)

    actions_on_top = True
    form_layout=(
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content'
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('cus_admin:blog_post_change', args=(obj.id,))
            reverse('xadmin:blog_post_change', args=(obj.id, ))
        )

    operator.short_description = '操作'

    # @property
    # def media(self):
    #     media  = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),})
    #
    #     return media

    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',)
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


# xadmin 自带日志功能,不需要我们自己来做了
# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin:
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
