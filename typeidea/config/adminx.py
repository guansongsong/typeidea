from django.contrib import admin
from . import models
from custom_site import custom_site
from base_admin import BaseOwnerAdmin
import xadmin
# Register your models here.


@xadmin.sites.register(models.Link, )
class LinkAdmin(BaseOwnerAdmin):
    list_display = ['title', 'href', 'status', 'weight', 'create_time']
    fields = ('title', 'href', 'status', 'weight')


@xadmin.sites.register(models.SideBar, )
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ['title', 'display_type', 'content', 'create_time']
    fields = ('title', 'display_type', 'content',)
