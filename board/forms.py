from django import forms
from django.contrib.auth.models import User, Group

from allauth.account.forms import SignupForm

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for create post"""
    class Meta:
        model = Post
        fields = [
            'category',
            'header',
            'text',
            'files',
        ]
        labels = {
            'category': 'Category',
            'header': 'Header',
            'text': 'Text',
            'files': 'Files',
        }


class CommentForm(forms.ModelForm):
    """Form for create comment"""
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
        labels = {
            'text': 'Text',
        }


class BasicSignupForm(SignupForm):
    """Form for signup"""
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        user_group = Group.objects.get(name='users')
        user_group.user_set.add(user)
        return user
