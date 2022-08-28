from django import forms
from django.forms import ModelForm
from .models import Post,Group
from captcha.fields import CaptchaField

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        captcha = CaptchaField()




