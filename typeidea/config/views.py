from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Link
from blog.views import CommontViewMixin


# Create your views here

class LinksView(CommontViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    # model = Link

    template_name = 'config/links.html'
    context_object_name = 'link_list'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'links': self.get_queryset()
    #     })
    #     return context
    #
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(status=Link.STATUS_NORMAL).order_by('-weight')


