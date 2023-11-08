from django.urls import path
from . import views 
urlpatterns = [
 path('inicio/', views.index, name='inicio' ),
 path("python/", views.pythonpost , name="python"),
 path('', views.combined_login_register_view, name='login'),
 path('logout/', views.logout_view, name='logout'),
 path('foro/', views.foro, name='foro'),
 path('post/<int:pk>/', views.post_details, name='post_details'),
 path('newpost', views.create_post, name='create_post'),
 path('like/post/<int:post_id>/', views.like_post, name='like_post'),
path('search/advanced/', views.advanced_search, name='advanced_search'),
 path('search/', views.search_results, name='search_results')

 ]