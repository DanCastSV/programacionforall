from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Corregido: self.title en lugar de self.titulo
        super().save(*args, **kwargs)

class Comment (models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"comentario de {name} {content}"