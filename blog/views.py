from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect


authors = [
    {'username': 'John Paul', 'email': 'pool@google.com', 'num_posts': 3},
    {'username': 'Arthur Morgan', 'email': 'morg@google.com', 'num_posts': 13},
    {'username': 'Anthony Morris', 'email': 'tony@google.com', 'num_posts': 8},
]


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    if pk >= 3:
        uri = reverse(post_new)
        return redirect(uri)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_publishers(request):
    data = {'authors': authors}
    return render(request, 'blog/publishers.html', context=data)
