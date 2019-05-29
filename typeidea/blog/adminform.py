from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label="摘要", required=False)
    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='category-autocomplete'),
    #     label='分类',
    # )
    # tag = forms.ModelChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='tag-autocomplete'),
    #     label='标签',
    # )
    #
    # class Meta:
    #     model = Post
    #     fields = ('category', 'tag', 'title', 'desc', 'content', 'status')

    # django-autocomplete-light新手指南：http://django-autocomplete-light.readthedocs.io/en/master/tutoial.html
    content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')
