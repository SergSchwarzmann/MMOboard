from django.contrib import admin
from django.urls import path

from .views import Welcome, PostList, PostDetail, PostCreate, PostUpdate, PostDelete, CategoryListView, ProfileView, \
    CommentCreate, comment_approve, comment_delete, AuthorPostList

urlpatterns = [
    path('', Welcome.as_view(), name='welcome'),
    path('posts/', PostList.as_view(), name='postlist'),
    path('posts/<int:pk>', PostDetail.as_view(), name='postdetail'),
    path('posts/create/', PostCreate.as_view(), name='postcreate'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='postupdate'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='postdelete'),
    path('category/<int:pk>/', CategoryListView.as_view(), name='categorylist'),
    path('profile/', ProfileView.as_view(), name='profilepage'),
    path('posts/<int:post_id>/commentcreate/', CommentCreate.as_view(), name='commentcreate'),
    path('comment/<int:pk>/approve/', comment_approve, name='commentapprove'),
    path('comment/<int:pk>/delete/', comment_delete, name='commentdelete'),
    path('posts/author_posts', AuthorPostList.as_view(), name='authorpostlist'),
]