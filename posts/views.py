from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from .models import Post,Group
from django.contrib.auth.decorators import login_required
#from .forms import CreationForm
from .forms import PostForm


def index(request):
    latest = Post.objects.order_by("-pub_date")[:11]
    return render(request, "index.html", {"posts": latest})

def group_posts(request, slug=None):
    group = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group = group).order_by("-pub_date")[:12]
    context = {"group": group, "posts": posts}

    return render(request, "group.html",context)

#@login_required()
class PostNew(CreateView):
    form_class = PostForm
    success_url = "/"
    template_name = "new.html"
