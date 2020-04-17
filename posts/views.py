from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    latest = Post.objects.order_by("-pub_date")[:11]
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")

        return render(request, "new_post.html", {"form": form})

    form = PostForm()
    return render(request, "new_post.html", {"form": form})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, id=post_id)
    return render(request, 'post.html', {'posts': posts,
                                         'author': author})


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

