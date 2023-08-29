from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm
# Create your views here.


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio/')  
        else:
            # Mostrar un mensaje de error
            pass
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def foro(request):
    post = Post.objects.all().order_by('-id')

    return render(request, 'foro.html',{'post':post})

def post_details(request, post_id):
    post = Post.objects.get(id=post_id)

    return render(request, 'post_details.html', {'post':post})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('foro')  # Cambia 'inicio' por la URL adecuada
    else:
        form = PostForm()
    return render(request, 'newpost.html', {'form': form})
