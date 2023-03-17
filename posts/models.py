from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from group.models import Group




class Post(models.Model):
    text = models.TextField(help_text='Текст вашей записи', verbose_name='Текст')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete= models.SET_NULL, related_name= "posts", blank= True, null= True, verbose_name='Группа')
    #likes = GenericRelation(Like)
    like = models.ManyToManyField(get_user_model(), blank=True, related_name='like')
    # поле для картинки
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    created = models.DateTimeField('date published', auto_now_add=True,
                                   db_index=True)
    text = models.TextField()

    class Meta:
        ordering = ('created',)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ["-pub_date"]
        unique_together = ["user", "author"]

class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liker',
        verbose_name='Пользователь',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='liked',
        verbose_name='Пост'
    )

    def __str__(self):
        return f'{self.user} -> {self.post}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ['user', 'post']




