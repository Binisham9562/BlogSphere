from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post, Comment, Like, Dislike
from .forms import PostForm,CommentForm 
from userapp.models import Category,Profile
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from .models import Post, Category

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        posts = posts.filter(title__icontains=search_query) | posts.filter(content__icontains=search_query)

    category_id = request.GET.get('category', None)
    if category_id:
        posts = posts.filter(category_id=category_id)

    return render(request, 'blogapp/post_list.html', {
        'posts': posts,
        'categories': categories,
    })    

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post was created successfully!')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blogapp/create_post.html', {'form': form})

@login_required
def user_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blogapp/user_profile.html', {
        'user_profile': user_profile,
        'user_posts': user_posts
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment was added successfully!')
            return redirect('post_detail', post_id=post.id)
    return render(request, 'blogapp/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def edit_post(request, post_id, category_id):
    # Fetch the post and category
    post = get_object_or_404(Post, id=post_id)
    category = get_object_or_404(Category, id=category_id)

    # Check if the user is the author of the post
    if request.user != post.author:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('post_list')

    # Ensure that the post belongs to the current category
    if post.category != category:
        messages.error(request, "This post does not belong to the current category.")
        return redirect('category_posts', category_id=category.id)

    # Handle the form submission
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post was updated successfully!')
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'blogapp/edit_post.html', {'form': form, 'category': category})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Your post was deleted successfully.')
    return redirect('post_list')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if created:
        messages.success(request, f'You liked "{post.title}".')
    else:
        like.delete()
        messages.info(request, f'You removed your like from "{post.title}".')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    dislike, created = Dislike.objects.get_or_create(post=post, user=request.user)
    if created:
        messages.warning(request, f'You disliked "{post.title}".')
    else:
        dislike.delete()
        messages.info(request, f'You removed your dislike from "{post.title}".')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    categories = Category.objects.all()  # Fetch all categories to display in the sidebar
    return render(request, 'blogapp/category_posts.html', {
        'posts': posts,
        'category': category,
        'categories': categories,  # Pass categories to the template
    })

def search_posts(request):
    username = request.GET.get('username', '')
    if username:
        user = User.objects.filter(username__icontains=username).first()
        if user:
            posts = Post.objects.filter(author=user)
        else:
            posts = Post.objects.none()  # No posts if no user is found
    else:
        posts = Post.objects.all()

    return render(request, 'blogapp/search_posts.html', {'posts': posts})