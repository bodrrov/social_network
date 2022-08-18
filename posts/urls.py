from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.group_posts),
    path("new_post/", views.PostNew.as_view(), name = 'new'),
]