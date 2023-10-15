from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm, CommentForm, CustomPostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
# Create your views here.





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

@login_required

def index(request):

    return render(request, "index.html")

@login_required
def pythonpost(request):
    return render(request, "python.html")

@login_required
def foro(request):
    #muestra los post del foro 
    post = Post.objects.all().order_by('-id')#hace que el post se muestre de manera ordenada 

    return render(request, 'foro.html',{'post':post})

@login_required
def post_details(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.filter()

        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'like':
                post.like(request.user)
            elif action == 'unlike':
                post.unlike(request.user)
            elif action == 'comment':
                form = CommentForm(request.POST)
                if form.is_valid():
                    new_comment = form.save(commit=False)
                    new_comment.post = post
                    new_comment.user = request.user
                    new_comment.save()

        form = CommentForm()

        return render(request, 'post_details.html', {'post': post, 'comments': comments, 'form': form})
    
    except:
        return render(request, '404.html')




@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Guarda el formulario solo si es válido
            post = form.save(commit=False)
            post.author = request.user  # Asigna el autor del post
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm()  # Crea una instancia del formulario vacío

    return render(request, 'newpost.html', {'form': form})


@login_required
def like_post(request, post_id):
    try:
        # Obtén la publicación por su ID
        post = Post.objects.get(pk=post_id)

        # Incrementa el contador de likes
        post.likes += 1
        post.save()

        return redirect('post_details', pk=post_id)

    except Post.DoesNotExist:
        # Manejar el caso en el que no se encuentra la publicación
        # Puedes redirigir a una página de error o realizar alguna otra acción adecuada
        pass
    
   
