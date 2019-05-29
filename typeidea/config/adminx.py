from django.contrib import admin

import xadmin

# Register your models here.
from .models import Link, SideBae
from custom_site import custom_site
from base_admin import BaseOwnerAdmin


@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'create_time')
    fields = ('title', 'href', 'status', 'weight')


@xadmin.sites.register(SideBae)
class SideBaeAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'status', 'create_time')
    fields = ('title', 'display_type', 'content', 'status')
