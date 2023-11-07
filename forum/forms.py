from django import forms
from ckeditor.widgets import CKEditorWidget 
from .models import Post, Comment, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
       
        if not any(char.isdigit() for char in password1):
            raise ValidationError("La contraseña debe contener al menos un dígito.")
        if not any(char.isalpha() for char in password1):
            raise ValidationError("La contraseña debe contener al menos una letra.")

        
        return password2

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(widget=forms.HiddenInput())
    content = forms.CharField(widget=CKEditorWidget())
    image = forms.ImageField(label= "avatar",required=False,widget=forms.FileInput(attrs={'class':'form-control'}))  # Campo de imagen opcional
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
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
        fields = ['title', 'slug', 'content', 'image', 'tags']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu comentario aquí'}),
        max_length=15000,  # Ajusta la longitud máxima según tus necesidades
        label='Comentario'
    )

    class Meta:
        model = Comment
        fields = ('content',)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Este campo es requerido')
        return content

