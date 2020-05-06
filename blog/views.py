from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from django.views.generic import ListView
from django.views.generic.dates import MonthArchiveView, WeekArchiveView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    page = request.GET.get('page', 1)
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, "home.html", {'post_list': post_list})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        page = request.GET.get('page', 1)
        posts = Post.objects.filter(
            Q(title__contains=query) | Q(text__contains=query)).distinct()
        paginator = Paginator(posts, 10)
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'search.html', {'post_list': post_list})
    else:
        return render(request, "search.html", {'post_list': []})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


@user_passes_test(lambda u: u.is_superuser)
def post(request):
    post_list = Post.objects.all()
    return render(request, 'post.html', {'post_list': post_list})


@user_passes_test(lambda u: u.is_superuser)
def add_post(request, id=None):
    instance = get_object_or_404(Post, id=id) if id is not None else None
    form = PostForm(request.POST or None, instance=instance)
    title = "Edit Post" if id is not None else "Add Post"

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('edit_post',
                        id) if id is not None else redirect('add_post')
    return render(request, 'add_post.html', {'form': form, 'title': title})


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.prev_post = (Post.objects.filter(id__lt=post.id).first())
    post.next_post = (Post.objects.filter(id__gt=post.id).first())
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        request.session["name"] = comment.name
        request.session["email"] = comment.email
        request.session["website"] = comment.website
        return redirect(request.path)
    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')
    form.initial['website'] = request.session.get('website')
    return render(request, 'view_post.html', {
        'post': post,
        'form': form,
    })


class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "created_at"
    allow_future = True


class PostWeekArchiveView(WeekArchiveView):
    queryset = Post.objects.all()
    date_field = "created_at"
    week_format = "%W"
    allow_future = True