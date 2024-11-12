from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib import messages
from django.contrib.auth.models import User
from blogapp.models import Post, Category
from .forms import UserRegistrationForm,CustomLoginForm,ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import Profile

@login_required
def home(request):
    posts = Post.objects.all()  # Fetch all posts, or use filtering to display posts by the logged-in user
    categories = Category.objects.all() 
    return render(request, 'blogapp/post_list.html',{'posts': posts, 'categories': categories})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'userapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Check if the user has a profile, if not, redirect to the profile creation page
                try:
                    user.profile
                except Profile.DoesNotExist:
                    return redirect('create_profile')  # Redirect to the profile creation page if no profile exists

                return redirect('post_list')  # Redirect to the post list if user has a profile
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'userapp/login.html', {'form': form})

@login_required
def create_profile(request):
    # Check if the user already has a profile
    try:
        user_profile = request.user.profile
        return redirect('post_list')  # If profile exists, redirect to the post list
    except Profile.DoesNotExist:
        # If the user does not have a profile, show the profile creation form
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Your profile has been created successfully.')
                return redirect('post_list')  # Redirect to posts list after profile creation
        else:
            form = ProfileForm()

    return render(request, 'userapp/create_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('frontpage')

def frontpage(request):
    return render(request,'userapp/frontpage.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'userapp/password_reset.html'
    email_template_name = 'userapp/password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = '/userapp/password_reset/done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'userapp/password_reset_done.html'

@login_required
def protected_view(request):
    return render(request, 'userapp/protected.html')

