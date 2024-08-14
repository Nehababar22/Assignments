from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, InterestForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import HttpResponseBadRequest
from .models import Interest

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

@login_required
def send_interest(request, id):
    """
    Send an interest request to another user.

    Handles POST requests to create an interest instance. Redirects to the user list page after sending the interest.
    """
    receiver = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.sender = request.user
            interest.receiver = receiver
            interest.save()
            
            return redirect('user-list')
    else:
        form = InterestForm()
    
    return render(request, 'interests/send_interest.html', {'form': form, 'receiver': receiver})

@login_required
def interest_list(request):
    """
    Display a list of interests for the logged-in user.

    Shows received interests that are not accepted and sent interests.
    """
    received_interests = Interest.objects.filter(receiver=request.user, accepted=False)
    sent_interests = Interest.objects.filter(sender=request.user)
    return render(request, 'interests/interest_list.html', {
        'received_interests': received_interests,
        'sent_interests': sent_interests
    })

@login_required
def view_interests(request):
    """
    Displays interests that are neither accepted nor rejected.
    """
    interests = Interest.objects.filter(receiver=request.user, accepted=False, rejected=False)
    return render(request, 'interests/view_interests.html', {'interests': interests})

@login_required
def handle_interest(request, interest_id, action):
    """
    Handle an interest request.

    Accepts or rejects an interest based on the action parameter. Redirects to the appropriate page after handling.
    """
    interest = get_object_or_404(Interest, id=interest_id, receiver=request.user)
    
    if action == 'accept':
        interest.accepted = True
        interest.pending = False
        interest.save()
        return redirect('chat-page')  
    elif action == 'reject':
        interest.rejected = True
        interest.pending = False
        interest.save()
        return redirect('user-list') 
    else:
        # Handle invalid action
        return HttpResponseBadRequest('Invalid action')