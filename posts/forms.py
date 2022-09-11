from django import forms
from django.forms import ModelForm
from .models import Post, Comment
from captcha.fields import CaptchaField

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        captcha = CaptchaField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        text = forms.CharField(widget=forms.Textarea)
        labels = {
            'text': 'Комментарий'
        }
        help_texts = {
            'text': 'Напишите комментарий тут :)'
        }





