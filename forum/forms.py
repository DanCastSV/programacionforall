from django import forms
from ckeditor.widgets import CKEditorWidget 
from .models import Post, Comment

class PostForm(forms.ModelForm):
   # Define el formulario para el post
   from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(widget=forms.HiddenInput())
    content = forms.CharField(widget=CKEditorWidget())
    image = forms.ImageField(required=False)  # Campo de imagen opcional

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 10:
            raise forms.ValidationError("El contenido debe tener al menos 10 caracteres.")
        return content

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'image']


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
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Este campo es requerido')
        return content

