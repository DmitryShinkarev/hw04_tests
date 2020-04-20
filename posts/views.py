from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    quantity = Post.objects.filter(group=group).count()
    return render(request, "group.html", {"group": group, "page": page,
                                          'paginator': paginator,
                                          'quantity': quantity})


@login_required
def new_post(request):
    button = "Создать"
    title = "Новая запись"
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            author = request.user
            pub_date = timezone.now()
            post = Post.objects.create(text=text, pub_date=pub_date, author=author, group=group)
            return redirect('post:index')
        return render(request, "new_post.html", {"form": form, 'button': button, 'title': title})
    form = PostForm()
    return render(request, 'new_post.html', {'form':form, 'button': button, 'title': title})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    quantity = Post.objects.filter(author=author).count()

    return render(request, 'post.html', {'posts': posts,
                                         'author': author,
                                         'paginator': paginator,
                                         'quantity': quantity})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, id=post_id)
    quantity = Post.objects.filter(author=author).count()
    return render(request, 'post.html', {'posts': posts,
                                         'author': author,
                                         'quantity': quantity})


def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author = profile.pk)
    button = "Сохранить"
    title = "Редактирование записи"
    if request.method == "GET":
        if request.user.username != username:
             return redirect('post:post', username=post.author, post_id=post.pk)
        form = PostForm(instance=post)
        return render(request, 'new_post.html', {'form': form, 'button': button, 'title': title, 'post': post})
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if request.user.username == username:
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post:post', username=post.author, post_id=post.pk)
            return render(request, 'new_post.html', {'form': form, 'button': button, 'title': title, 'post': post})
        return redirect('post:post', username=post.author, post_id=post.pk)