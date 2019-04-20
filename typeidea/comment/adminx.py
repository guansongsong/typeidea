from django.contrib import admin
from . import models
from custom_site import custom_site
from base_admin import BaseOwnerAdmin
import xadmin
# Register your models here.


@xadmin.sites.register(models.Comment, )
class CommentAdmin:
    list_display = ('target', 'nickname', 'content', 'website', 'create_time')

