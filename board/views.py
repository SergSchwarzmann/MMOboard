from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from itertools import chain

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


class Welcome(TemplateView):
    template_name = 'welcome.html'


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    # def get_queryset(self):
    #     return Post.objects.filter(author = self.request.user)


class AuthorPostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'author_posts.html'
    context_object_name = 'authorposts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_posts = Post.objects.filter(author=self.request.user)
        context['author_posts'] = author_posts
        return context


class PostDetail(DetailView):
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
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['header'])
        obj.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('postlist')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class CategoryListView(ListView):
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
    template_name = 'account/profile.html'

    # def get_queryset(self):
    #     queryset = Post.objects.filter(author=request.user.author, comment__approve=False)
    #     print(queryset)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_approve = Post.objects.filter(author=self.request.user, comments__approve=False).distinct()
        context['post_approve'] = post_approve
        return context



class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     return context

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
    com = Comment.objects.get(id=pk)
    com.approve = True
    com.save()
    return redirect(f'/posts/{com.post.id}')

@login_required
def comment_delete(request,pk):
    com = Comment.objects.get(id=pk)
    com.delete()
    return redirect(f'/posts/{com.post.id}')
