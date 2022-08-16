from django.db import models
from django.contrib.auth import get_user_model
user= get_user_model()

# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length= 200)
    slug = models.SlugField(unique= True)
    description = models.TextField()

    def __str__(self):
        return self.title
