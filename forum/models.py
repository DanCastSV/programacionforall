from django.db import models
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
