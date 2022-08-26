from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from .models import Post,Group
from django.contrib.auth.decorators import login_required
#from .forms import CreationForm
from .forms import PostForm
from django.core.paginator import Paginator
from telebot.sendmessage import sendTelegram


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
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post_new = form.save(commit=False)
        post_new.author = request.user
        post_new.save()
        return redirect('index')
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User,
                             username=username)
    post_list = user.posts.all()
    paginator = Paginator(post_list, 10)
    post_count = paginator.count
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {
            'profile': user,
            'post_list': post_list,
            'my_posts': post_count,
            'paginator': paginator,
            'page': page
        })


def post_view(request, username, post_id):
    post = get_object_or_404(Post.objects.select_related('author'),
                             id=post_id, author__username=username)
    form = CommentForm()
    comments = post.comments.all()
    author = post.author
    return render(
        request,
        'post.html',
        {'post': post, 'author': author, 'comments': comments, 'form': form}
    )

@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             author__username=username)

    if request.user != post.author:
        return redirect('post',
                        username=username,
                        post_id=post_id)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post',
                        username=username,
                        post_id=post_id)

    return render(request,
                  'new_post.html',
                  {'form': form,
                   'post': post
                   }
                  )


def thanks(request):
    if request.POST:
        author = request.POST['author']
        group = request.POST['group']
        text = request.POST['text']
        element = Post(author=author,group=group, pub_date=pub_date, text =text)
        element.save()
        sendTelegram(tg_author=author, tg_pub_date=pub_date, tg_text=text, tg_group=group)
        return render(request, './index.html', {'author': author})
    else:
        return render(request, './index.html')