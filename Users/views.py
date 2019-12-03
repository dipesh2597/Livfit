from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import RegisterForm

def index(request):
    return render(request, 'user/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')# for getting username into username variable
            password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password1)
            login(request, user)
            messages.success(request, f'Your account has been created for {username}! Now you are logged in!') # will print success message by a variable {{ message }} in html
            return redirect('home-index')
    else:
        form = RegisterForm() #only for testing but please create a specific registerpage with a nice look
    return render(request, 'user/register.html', {'form': form})

    request.login_form = form

@login_required
def profile(request):
    return render(request, 'user/profile.html')








