from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# Create your views here.
def register(request):
    """
    Handle user registration.

    Handles POST requests to register a new user. If the username already exists,
    an error is added to the form. On successful registration, redirects to login page.
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists.')
            else:
                try:
                    form.save()
                    return redirect('login')
                except IntegrityError:
                    form.add_error(None, 'An error occurred while creating your account. Please try again later.')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """
    Handle user login.

    Handles POST requests to authenticate and log in a user. On successful login,
    redirects to the user list page.
    """

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user-list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    """
    Handle user logout.

    Logs out the user and redirects to the login page.
    """

    logout(request)
    return redirect('login')

@login_required
def user_list(request):
    """
    Display a list of users.
    """

    users = User.objects.exclude(id=request.user.id)    
    return render(request, 'users/user_list.html', {'users': users})

