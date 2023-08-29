from django.urls import path
from . import views 
urlpatterns = [
 path('inicio/', views.index, name='inicio' ),
 path('', views.login_view, name='login'),
 path('register/', views.register_view, name='register'),
 path('logout/', views.logout_view, name='logout'),
 path('foro/', views.foro, name='foro'),
 path('<int:post_id>',  views.post_details, name='post_details'),
 path('newpost', views.create_post, name='create_post')
 ]