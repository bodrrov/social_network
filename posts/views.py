from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from social_core.backends import username
from .models import Post,Group,User, Follow
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from telebot.sendmessage import sendTelegram


def index(request):
    post_list = Post.objects.order_by('-pub_date').all() #сортировка записей
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page,
         'paginator': paginator}
    )

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug) #функция ищет объект модели,а если не находит error 404
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
        group= get_object_or_404(Group, pk=post_new.group_id)
        image = Post.objects.get(image=post_new.image)
        sendTelegram(tg_text = post_new, tg_author = post_new.author,tg_group= group,tg_image= image)
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
    following = False
    if request.user.is_authenticated:
        following = user.following.filter(user=request.user).exists()
    return render(
        request,
        'profile.html',
        {
            'profile': user,
            'post_list': post_list,
            'my_posts': post_count,
            'paginator': paginator,
            'page': page,
            'following': following,
            'user': user,
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
    """ Обрабатывает страницу редактирования записи """
    user_profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=user_profile)
    if request.user != post.author:
        return redirect(f'/{username}/{post_id}/')
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'/{username}/{post_id}/')
    return render(request, 'new_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request,username, post_id):
    user_profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=user_profile)
    post.delete()
    return render(request, 'post.html', {'post': post, 'username': username})

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
    post_list = ( Post.objects.select_related('author').filter(author__following__user=request.user))
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
    """ Обрабатывает POST-запрос кнопки "Подписаться", добавляет автора в подписку """
    if request.user.username != username:
        author = get_object_or_404(User, username=username)
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)

@login_required
def profile_unfollow(request, username):
    """ Обрабатывает POST-запрос кнопки "Отписаться", удаляет автора из подписки """
    author = get_object_or_404(User, username=username)
    author.following.filter(user=request.user).delete()
    return redirect('profile', username=username)

def telebot(request):
    if request.POST:
        author = request.POST['author']
        text = request.POST['text']
        sendTelegram(tg_author=author, tg_text=text, tg_group=group)
        return render(request, './index.html', {'author': author,'text': text,})
    else:
        return render(request, './index.html')

