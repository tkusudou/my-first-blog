from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm

logger = logging.getLogger(__name__)

class inquiry(generic.FormView):
    template_name="inquiry.html"
    form_class=InquiryForm

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if 'save' in request.POST:
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        if 'delete' in request.POST:
            return redirect('post_delete', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'post':post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if "yes" in request.POST:
            post = Post.objects.get(pk=pk)
            post.delete()
            return redirect('post_list')
        if "cancel" in request.POST:
            return redirect('post_edit', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_delete.html', {'post': post})
    


