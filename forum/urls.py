from django.urls import path
from . import views 
urlpatterns = [
 path('inicio/', views.index, name='inicio' ),
 path("python/", views.pythonpost , name="python"),
 path('', views.login_view, name='login'),
 path('register/', views.register_view, name='register'),
 path('logout/', views.logout_view, name='logout'),
 path('foro/', views.foro, name='foro'),
 path('post/<int:pk>/', views.post_details, name='post_details'),
 path('newpost', views.create_post, name='create_post'),
 path('like/post/<int:post_id>/', views.like_post, name='like_post')

 ]