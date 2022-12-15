from django.contrib import admin
from django.urls import path
from .views import Welcome, PostList, PostDetail, PostCreate, PostUpdate, PostDelete, CategoryListView

urlpatterns = [
    path('', Welcome.as_view(), name='welcome'),
    path('posts/', PostList.as_view(), name='postlist'),
    path('posts/<int:pk>', PostDetail.as_view(), name='postdetail'),
    path('posts/create/', PostCreate.as_view(), name='postcreate'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='postupdate'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='postdelete'),
    path('category/<int:pk>/', CategoryListView.as_view(), name='categorylist'),
]