from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from .models import Post,Group
from django.contrib.auth.decorators import login_required
#from .forms import CreationForm
from .forms import PostForm
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )
def group_posts(request, slug=None):
    group = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group = group).order_by("-pub_date")[:12]
    paginator = Paginator(posts, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    context = {"group": group, "posts": posts}

    return render(request, "group.html",context, {'page': page, 'paginator': paginator})

#@login_required()
#class PostNew(CreateView):
    #form_class = PostForm
    #success_url = "/"
    #template_name = "new.html"

@login_required()
def new_post(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'new.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')

