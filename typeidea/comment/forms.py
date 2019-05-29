import mistune
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )
    email = forms.EmailField(
        label='邮箱',
        max_length=126,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%'}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=126,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%'}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=1024,
        widget=forms.widgets.Textarea(
            attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 10:
            raise forms.ValidationError('内容长度太短了。')
        return mistune.markdown(content)

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']
