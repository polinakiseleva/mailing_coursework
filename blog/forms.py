from blog.models import Blog
from django import forms

from mailing.forms import StyleFormMixin


class BlogPostForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
