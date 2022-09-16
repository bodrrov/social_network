from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from .models import Post,Group,User, Follow
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
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

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "group.html",
        {
            "group": group,
            "posts": posts,
            'paginator': paginator,
            'page': page
        }
    )

@login_required()
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)  #инициализация формы
    if request.method == 'POST' and form.is_valid():  #проверка на валидацию и проверка на запрос от пользователя
        post_new = form.save(commit=False)  #commit= False вернет объект,не сохраненный в базу данных
        post_new.author = request.user
        post_new.save()
        sendTelegram(tg_text=post_new, tg_author=request.user)
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User,
                             username=username)
    post_list = user.posts.all()
    paginator = Paginator(post_list, 10)
    post_count = paginator.count
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'profile.html',
        {
            'profile': user,
            'post_list': post_list,
            'my_posts': post_count,
            'paginator': paginator,
            'page': page
        }
    )

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
                   'post': post,
                   'edit':True
                   }
                  )
@login_required
def delete_post(request,post_id=None):
    post_to_delete=Post.objects.get(id=post_id)
    post_to_delete.delete()
    return HttpResponseRedirect(request, '/index.html')


def telebot(request):
    if request.POST:
        author = request.POST['author']
        group = request.POST['group']
        text = request.POST['text']
        #element = (author=author,group=group, pub_date=pub_date, text =text)
        element.save()
        sendTelegram(tg_author=author, tg_pub_date=pub_date, tg_text=text, tg_group=group)
        return render(request, './index.html', {'author': author},  {'text': text})
    else:
        return render(request, './index.html')

def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )

def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, post_id, username):
    post = get_object_or_404(Post,
                             pk=post_id,
                             author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        form.save()
        return redirect('post', username, post_id)
    return redirect('post', username, post_id)


@login_required
def follow_index(request):
    author = get_object_or_404(User, username=request.user.username)
    post_list = (
        Post.objects.select_related('author').filter(
            author__following__user=request.user)
    )
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  "follow.html",
                  {
                      "paginator": paginator,
                      "page": page,
                      "author": author

                  })

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(user=request.user, author=author)
    if following.exists():
        following.delete()
    return redirect('follow_index')

