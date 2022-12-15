from django import forms
from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'header',
            'text',
        ]
        labels = {
            'category': 'Category',
            'header': 'Header',
            'text': 'Text'
        }