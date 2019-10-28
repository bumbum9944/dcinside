from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.db.models import Q

# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-id')
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)


def detail(request, id):
    post = get_object_or_404(Post, id=id)
    posts = Post.objects.all().order_by('-id')
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)


@login_required
def update(request, id):
    post = get_object_or_404(Post, id=id)
    if post.user == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:detail', id)
        else:
            form = PostForm(instance=post)
        context = {
            'form': form,
        }
        return render(request, 'posts/form.html', context)
    else:
        return redirect('posts:detail', id)


@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.user == request.user:
        if request.method == 'POST':
            post.delete()
            return redirect('posts:index')
    else:
        return redirect('posts:detail', id)


@login_required
def comment_create(request, post_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post_id = post_id
            comment.save()
            return redirect('posts:detail', post_id)


@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
    return redirect('posts:detail', post_id)
    

def search(request):
    target = request.GET.get('search')
    posts = Post.objects.all().filter(Q(title__contains=target) | Q(content__contains=target)).order_by('-id')
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)
    
def like(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if post.like_users.filter(id=user.id):
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:detail', id)

def hate(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if post.hate_users.filter(id=user.id):
        post.hate_users.remove(user)
    else:
        post.hate_users.add(user)
    return redirect('posts:detail', id)