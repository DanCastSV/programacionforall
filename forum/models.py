from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    created_on = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    image = models.ImageField(upload_to='imagenes', null=True, blank=True)  # Campo de imagen opcional
    likes = models.ManyToManyField(User, related_name='liked_posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Corregido: self.title en lugar de self.titulo
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

    
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')



