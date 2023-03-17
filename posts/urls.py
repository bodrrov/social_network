from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/like/', views.post_like, name='post_like'),
    path('posts/<int:post_id>/unlike/', views.post_unlike, name='post_unlike'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('new/', views.new_post, name='new-post'),
    path('follow/', views.follow_index, name='follow_index'),
    path('<str:username>/follow/', views.profile_follow,
         name="profile_follow"),
    path('<str:username>/unfollow/', views.profile_unfollow,
         name='profile_unfollow'),
    path('<str:username>/', views.profile, name='profile'),
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'comment/<int:comment_id>/del',
        views.del_comment,
        name='del_comment'
    ),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),





]