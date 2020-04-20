from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(text=form.cleaned_data['text'],
                                group=form.cleaned_data['group'],
                                author=request.user)
            return redirect('index')
        return render(request, 'new_post.html', {'form': form})
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


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
    edited_post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=edited_post)
        if form.is_valid():
            edited_post.text = form.cleaned_data['text']
            edited_post.group = form.cleaned_data['group']
            edited_post.save()
            return redirect('index')
        return render(request, 'new_post.html', {'form': form})
    form = PostForm(instance=edited_post)
    edit = True
    return render(request, 'new_post.html', {'form': form,
                                             'edit': edit})