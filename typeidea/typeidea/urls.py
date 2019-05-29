"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from custom_site import custom_site
from blog.views import (
    IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView, post_list
)
from blog.rss import LatestPostFeed
from blog.apis import PostViewSet, post_view

# from blog.views import post_list, PostDetailView
from config.views import LinksView
from comment.views import CommentView
from .autocomplete import CategoryAutocomplete, TagAutocomplete

from typeidea.settings import develop as settings

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')

urlpatterns = [
    path('super_admin/', admin.site.urls),
    # path('admin/', custom_site.urls, name="admin"),
    url(r'^admin/', xadmin.site.urls, name="xadmin"),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    # url(r'^post/(?P<pk>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<owner_id>\d+)$', AuthorView.as_view(), name='author'),
    url(r'^links/$', LinksView.as_view(), name='links'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),

    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),

    url(r'^api/post/', post_view, name='post-list'),
    # url(r'^api/', include(router.urls, namespace="api")),
    url(r'^api/docs/', include_docs_urls(title='typeidea.apis')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
