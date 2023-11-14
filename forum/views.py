from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm, CommentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
# Create your views here.





def combined_login_register_view(request):
    context = {
        'login_form': {},  # Si tienes un formulario de inicio de sesión, reemplázalo aquí
        'register_form': CustomUserCreationForm(),
        'login_error': None,
    }

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                context['login_error'] = "Usuario o contraseña incorrecta"

        elif 'register_submit' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.email = register_form.cleaned_data['email']
                user.save()
                new_user = authenticate(username=register_form.cleaned_data['username'],
                                        password=register_form.cleaned_data['password1'])
                login(request, new_user)
                return redirect('inicio')
            else:
                context['register_form'] = register_form

    return render(request, 'combined_login_register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required

def index(request):

    return render(request, "index.html")

@login_required
def search_results(request):
    query = request.GET.get('query')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        posts = Post.objects.none()
    
    context = {
        'posts': posts,
    }
    return render(request, 'search_results.html', context)

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
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    form = CommentForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'like':
            if request.user not in post.likes.all():
                post.likes.add(request.user)
                
        elif action == 'unlike':
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                
        elif action == 'comment':
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
            else:
           
                print(form.errors)
                # Esto mostrará errores de validación en tu plantilla
                return render(request, 'post_details.html', {'post': post, 'comments': comments, 'form': form})

    return render(request, 'post_details.html', {'post': post, 'comments': comments, 'form': form})






@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Guarda las relaciones de many-to-many, como las etiquetas
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm()

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
        
        pass
    
@login_required

def advanced_search(request):
    query = request.GET.get('q', '')
    tag_query = request.GET.getlist('tags')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    if tag_query:
        posts = posts.filter(tags__name__in=tag_query).distinct()

    context = {
        'posts': posts,
        'query': query,
        'selected_tags': tag_query,
        'tags': Tag.objects.all(),
    }

    return render(request, 'advanced_search_results.html', context)
