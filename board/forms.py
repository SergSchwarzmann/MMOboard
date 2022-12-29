from django import forms
from django.contrib.auth.models import User, Group

from .models import Post, Comment

from allauth.account.forms import SignupForm


class PostForm(forms.ModelForm):

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

    # def save(self, request):
    #     user = super()

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'text',
        ]
        labels = {
            'text': 'Text',
        }


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        user_group = Group.objects.get(name='users')
        user_group.user_set.add(user)
        return user

