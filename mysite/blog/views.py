
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from .forms import PostForm,UserEditForm
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                      'blog/post/list.html',
                      {'page': page,
                       'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        # Create a new user object but avoid saving it yet
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            posts = Post.published.all()
            return render(request,
                          'blog/post/list.html',
                          {'posts': posts})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                      'blog/post/register.html',
                      {'user_form': user_form})

@login_required
def my_list(request):
    current_user = request.user
    object_list = Post.objects.filter(author=current_user)

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/my_list.html',
                  {'page': page,
                    'posts': posts})

@login_required
def post_create(request):

    if request.method == 'POST':
        # Form was submitted
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post = post_form.save()
            return render(request,
                          'blog/post/detail.html',
                          {'post': new_post})

    else:
        post_form = PostForm()
    return render(request, 'blog/post/new_post.html', {'post_form': post_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')



    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'registration/edit.html',
                  {'user_form': user_form})