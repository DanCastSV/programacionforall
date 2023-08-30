from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm, CommentForm
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

    comments = post.comments.filter(active=True)

    # Inicializa el formulario fuera de la declaración if
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.post = post
            nuevo_comentario.save()

    return render(request, 'post_details.html', {'post': post, 'comments': comments, 'form': form})



def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(title=form.cleaned_data["title"], slug=form.cleaned_data["slug"], content=form.cleaned_data["content"])
            post.save()
            return redirect("foro/")
    else:
        form = PostForm()
        print("papi algo esta fallando")  # Esto se mostrará en la consola del servidor

    return render(request, "newpost.html", {"form": form})
 