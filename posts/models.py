from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from group.models import Group

class Post(models.Model):
    text = models.TextField(help_text='Текст вашей записи', verbose_name='Текст')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete= models.SET_NULL, related_name= "posts", blank= True, null= True, verbose_name='Группа')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self):
        return self.text[:10]


