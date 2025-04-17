from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from register.forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()




@csrf_protect
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"register_user": form})




@csrf_protect
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                elif getattr(user, 'is_admin', False):
                    return redirect('superuser_home')
                else:
                    return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "register/login.html", {"login_user": form})




@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

