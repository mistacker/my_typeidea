from django.contrib import admin

import xadmin

# Register your models here.
from .models import Comment
from custom_site import custom_site
from base_admin import BaseOwnerAdmin

@xadmin.sites.register(Comment)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ['target', 'nickname', 'content', 'website', 'status', 'create_time']

# xadmin.site.register(Comment, CommentAdmin)