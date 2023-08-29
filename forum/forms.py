from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(widget=forms.HiddenInput())  # Ocultamos el campo slug
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content']
