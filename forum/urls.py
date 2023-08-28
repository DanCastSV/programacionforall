from django.urls import path
from . import views 
urlpatterns = [
 path('inicio/', views.index ),
 path('', views.login_view, name='login'),
 path('register/', views.register_view, name='register'),
 path('logout/', views.logout_view, name='logout')
 
]