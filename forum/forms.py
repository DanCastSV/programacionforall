from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    #se hace el formulario para el post 
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(widget=forms.HiddenInput())  # Ocultamos el campo slug
    content = forms.CharField()

    class Meta:
        
        model = Post
        fields = ['title', 'slug', 'content']

class CustomPostForm(PostForm):
    # se crea un nuevo formulario que extiende de la clase del modelo Post y agrega los campos a ser modificados en este
    class Meta:
        model = Post
        fields = ['title', 'slug']
        labels = {
            'title': 'Título:',
            'slug': 'Slug:',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

