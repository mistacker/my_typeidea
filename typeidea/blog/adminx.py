from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from xadmin.layout import Row, Fieldset
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
import xadmin

# Register your models here.
from .models import Category, Post, Tag
from .adminform import PostAdminForm
from custom_site import custom_site
from base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):  # 可选择继承admin.StackedInline，获取不同的展示样式
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'create_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数"


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')


class PostCategoryFilter(admin.SimpleListFilter):
    """
    自定义过滤器过滤非自己创建的分类
    """
    title = "分类过滤器"
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category = self.value()
        if category:
            return queryset.filter(category_id=self.value())
        return queryset


# 自定义过滤器category
class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)

# 简单实现一下has_add_permission的例子
import requests
from django.contrib.auth import get_permission_codename


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = ('title', 'desc', 'status', 'category', 'create_time', 'operate')

    # list_filter = (PostCategoryFilter,)
    list_filter = ('category',)
    search_fields = ('title', 'category__name')

    # fields = (
    #     ('title', 'category'),
    #     'desc',
    #     'content',
    #     'status',
    #     'tag',
    # )

    """
    fieldsets = (
        ('基础配置', {
            'description': "基础配置信息",
            'fields': ('title', 'category', 'status'),
        }),
        ('内容', {
            'fields': ('desc', 'content'),
        }),
        ('其他', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )
    """
    form_layout = (
        Fieldset(
            '基础配置',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容',
            'desc',
            'content',
        ),
        Fieldset(
            '其他',
            'tag',
        )
    )

    filter_horizontal = ('tag',)

    # filter_vertical = ('tag',)

    def operate(self, obj):
        return format_html(
            '<a href="{}">操作</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
            # self.model_admin_url('change', obj.id)
        )

    operate.short_description = "操作"

    # 增加静态资源的引入，就是自己写的css或者js代码
    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)
    #
    # PERMISSION_API = 'http://permission.sso.com/has_perm?user={}&perm_code={}'

    # 验证权限
    # def has_add_permission(self, request):
    #     opts = self.opts
    #     codename = get_permission_codename('add', opts)
    #     perm_code = "%s.%s" % (opts.app_label, codename)
    #     resp = requests.get(self.PERMISSION_API.format(request.user.username), perm_code)
    #     if resp.status_code == 200:
    #         return True
    #     else:
    #         return False


# xadmin.site.register(Category, CategoryAdmin)
# xadmin.site.register(Tag, TagAdmin)
# xadmin.site.register(Post, PostAdmin)
