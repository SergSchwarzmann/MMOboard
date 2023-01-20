from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User, Group
from django.conf import settings
import datetime
from django.utils import timezone

from itertools import chain

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


class Welcome(TemplateView):
    """Welcome page"""
    template_name = 'welcome.html'


class PostList(ListView):
    """All posts"""
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class AuthorPostList(ListView):
    """List of own posts for author"""
    model = Post
    ordering = '-date'
    template_name = 'author_posts.html'
    context_object_name = 'authorposts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_posts = Post.objects.filter(author=self.request.user)
        context['author_posts'] = author_posts
        return context


class PostDetail(DetailView):
    """View of post"""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=id)
        context['comments'] = post.comments.all()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    """Users create posts"""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['header'])
        obj.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    """Users edit/update their posts"""
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDelete(LoginRequiredMixin, DeleteView):
    """Users delete their posts"""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('postlist')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class CategoryListView(ListView):
    """List of post by categories"""
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """Authorized user profile"""
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_approve = Post.objects.filter(author=self.request.user, comments__approve=False).distinct()
        context['post_approve'] = post_approve
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    """Crate comment"""
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'

    def form_valid(self, form):
        id = self.kwargs.get('post_id')
        # pos = get_object_or_404(Post, id=id)
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=id)
        if form.instance.author == form.instance.post.author:
            form.instance.approve = True
        return super().form_valid(form)


@login_required
def comment_approve(request, pk):
    """Users approve comment on their posts"""
    com = Comment.objects.get(id=pk)
    com.approve = True
    com.save()
    return redirect(f'/posts/{com.post.id}')


@login_required
def comment_delete(request,pk):
    """Users delete comment on their posts"""
    com = Comment.objects.get(id=pk)
    com.delete()
    return redirect(f'/posts/{com.post.id}')


def weekly_mailing():
    """Weekly email post for last week"""
    today = timezone.datetime.now()
    # last_week = today - timezone.timedelta(minutes=10) #For testing purposes
    last_week = today - timezone.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    if posts:
        emails = list(User.objects.filter(groups__name='users').values_list('email', flat=True))
        html_content = render_to_string(
            'mails/weekly_post.html',
            {
                'link': f'{settings.SITE_URL}/posts/',
                'posts': posts,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Posts for the last week',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=emails,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    else:
        print('No posts for timedelta!')


def comment_notify(pk, preview, email, author_id):
    """Compose a notify about new comment"""
    html_content = render_to_string(
        'mails/comment_notify.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}',
            'prof_page_link': f'{settings.SITE_URL}/profile/',
        }
    )

    msg = EmailMultiAlternatives(
        subject='New comment to your post.',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email,],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
