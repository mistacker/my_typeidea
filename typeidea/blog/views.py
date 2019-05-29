from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

from .models import Tag, Category, Post
from config.models import SideBae

# from comment.form import CommentForm
# from comment.models import Comment

# Create your views here.


# def post_list(request, category_id=None, tag_id=None):
# content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(category_id=category_id, tag_id=tag_id)
# return HttpResponse(content)
# return render(request, 'blog/list.html', context={'name': 'post_list'})

# def post_detail(request, post_id=None):
# return HttpResponse('detail')
# return render(request, 'blog/detail.html', context={'name': 'post_detail'})

# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         try:
#             tag = Tag.objects.get(pk=tag_id)
#         except Tag.DoesNotExist:
#             post_list = []
#         else:
#             post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#
#     else:
#         post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             try:
#                 category = Category.objects.get(pk=category_id)
#             except Category.DoesNotExist:
#                 category = None
#             post_list = post_list.filter(category_id=category_id)
#
#     context = {
#         'tag': tag,
#         'category': category,
#         'post_list': post_list,
#     }
#
#     return render(request, 'blog/list.html', context=context)
"""
class T:
    pass


# 判断侧边栏的显示类型
def sidebars_content_html(sidebars):
    from comment.models import Comment
    ts = []
    for sidebar in sidebars:
        if sidebar.display_type == SideBae.DISPLAY_LATEST:
            context = {
                'posts': Post.latest_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context=context)
        elif sidebar.display_type == SideBae.DISPLAY_HOST:
            context = {
                'posts': Post.host_post()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context=context)
        elif sidebar.display_type == SideBae.DISPLAY_HTML:
            result = sidebar.content
        elif sidebar.display_type == SideBae.DISPLAY_COMMENT:
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context=context)
        else:
            result = None
        t = T()
        t.title = sidebar.title
        t.content_html = result
        ts.append(t)
    return ts


"""


# 侧边栏
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    sides = SideBae.get_all()

    context = {
        'tag': tag,
        'category': category,
        'post_list': post_list,
        # 'sidebars': sidebars_content_html(sides)
        'sidebars': sides
    }
    context.update(Category.get_navs())

    return render(request, 'blog/list.html', context=context)


# class PostDetailView(DeleteView):
#     model = Post
#     template_name = 'blog/detail.html'

"""
def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBae.get_all(),
    }

    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
"""


# 重构
# 重点！！！

class CommontViewMixin:
    def get_context_data(self, **kwargs):
        """
        把其他附加的数据放入context中显示到页面上
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBae.get_all()

        })
        context.update(Category.get_navs())
        return context


class IndexView(CommontViewMixin, ListView):
    queryset = Post.latest_posts()  # 指定当前View要使用的Model
    paginate_by = 5  # 一个页面显示的数据数量
    context_object_name = 'post_list'  # 如果不设置此项，模板中需要使用object_list变量
    template_name = 'blog/list.html'  # 页面


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
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
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


"""
class PostDetailView(CommontViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form': CommentForm,
    #         'comment_list': Comment.get_by_target(self.request.path)
    #     })
    #     return context

    def get(self, request, *args, **kwargs):
        # 想做什么就处理什么，不做的不处理
        # post_id = kwargs.get('post_id')
        # post = Post.objects.get(pk=post_id)
        # context = self.get_context_data()
        # context.update({
        #     'post': post,
        # })
        # post.PV += 1
        # post.UV += 1
        # post.save()
        # return render(request, self.template_name, context=context)
        response = super().get(request, *args, **kwargs)
        Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        return response
"""


class PostDetailView(CommontViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)  # 1分钟有效

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)  # 24小时有效

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


# 增加搜索的需求
class SearchView(IndexView):
    def get_queryset(self):
        qs = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return qs
        return qs.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword')
        })
        return context


# 增加作者页面
class AuthorView(IndexView):
    template_name = 'blog/author.html'
    context_object_name = 'author'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     owner_id = self.kwargs.get('owner_id')
    #     return qs.filter(owner_id=owner_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_id = self.kwargs.get('owner_id')
        author = get_object_or_404(User, pk=author_id)
        context.update({
            'author': author
        })
        return context
