from . import views
from django.urls import path

urlpatterns = [
    path('<username>/<int:post_id>/like/', views.add_like, name='add_like'),
    path('<username>/<int:post_id>/remove_like/', views.remove_like, name='remove_like'),
    path('<username>/<int:post_id>/is_fan/', views.is_fan, name='is_fan'),
    path('<username>/<int:post_id>/get_fans/', views.get_fans, name='get_fans'),

]