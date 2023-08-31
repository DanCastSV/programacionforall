from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    #se hace el formulario para el post 
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(widget=forms.HiddenInput())  # Ocultamos el campo slug
    content = forms.CharField()

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:  # Ejemplo de validación (mínimo 5 caracteres)
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 10:  # Ejemplo de validación (mínimo 10 caracteres)
            raise forms.ValidationError("El contenido debe tener al menos 10 caracteres.")
        return content

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
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Este campo es requerido')
        return content

