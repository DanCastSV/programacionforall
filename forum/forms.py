from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(widget=forms.HiddenInput())  # Ocultamos el campo slug
    content = forms.CharField()

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content']

class CommentForm(forms.ModelForm)   : 
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content', 'active')

