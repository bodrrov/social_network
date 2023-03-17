from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from social_core.backends import username
from .models import Post,Group,User, Follow,Like,Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from telebot.sendmessage import sendTelegram
from .utils import get_posts_context, get_authors_context
from taggit.models import Tag

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

def search(request):
    search = request.GET.get('q')
    context = get_posts_context(
        Post.objects.select_related('group', 'author').filter(
            text__icontains=search
        ),
        request
    )
    context['tags_colors'] = settings.TAGS_COLORS
    return render(request, 'posts/index.html', context)

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
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('post_detail', post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        form.save_m2m()
        return redirect('post_detail', post_id)

    context = {
        'form': form,
        'is_edit': True
    }
    return render(request, 'new_post.html', context)

def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    if author != request.user:
        return redirect('post_detail', post_id)
    else:
        post.delete()
        return redirect('profile', author.username)

def server_error(request):
    return render(request, "misc/500.html", status=500)



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post_detail', post_id=post_id)

@login_required
def del_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    author = comment.author
    if author != request.user:
        return redirect('post_detail', comment.post.id)
    else:
        comment.delete()
    return redirect('post_detail', comment.post.id)


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
    author = get_object_or_404(User, username=username)
    if (author != request.user
            and not request.user.follower.filter(author=author).exists()):
        Follow.objects.create(
            user=request.user,
            author=author
        )
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(
        author=get_object_or_404(User, username=username),
        user=request.user
    ).delete()
    return redirect('profile', username)

def telebot(request):
    if request.POST:
        author = request.POST['author']
        text = request.POST['text']
        sendTelegram(tg_author=author, tg_text=text, tg_group=group)
        return render(request, './index.html', {'author': author,'text': text,})
    else:
        return render(request, './index.html')

def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('group', 'author'),
        id=post_id
    )
    comments = post.comments.all()
    form = CommentForm()
    liked = (request.user.is_authenticated
             and request.user.liker.filter(post=post).exists())
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'liked': liked,
    }
    return render(request, 'post.html', context)

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if (post.author != request.user
            and not request.user.liker.filter(post=post).exists()):
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect('post_detail', post_id)

@login_required
def post_unlike(request, post_id):
    Like.objects.filter(
        post=get_object_or_404(Post, id=post_id),
        user=request.user
    ).delete()
    return redirect('post_detail', post_id)


