from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from transactions.models import Transaction
from .decorators import admin_required

User = get_user_model()

# Admin home
@admin_required
def superuser_home(request):
    return render(request, 'superuser/superuser_home.html')

# Lists all users
@admin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'superuser/user_list.html', {'users': users})

# Lists all transactions
@admin_required
def transaction_list(request):
    txs = Transaction.objects.select_related('sender', 'receiver')
    return render(request, 'superuser/transaction_list.html', {'txs': txs})

# Register new Admin
@admin_required
def create_superuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_admin = True  # promote to admin
            user.save()
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'superuser/create_superuser.html', {'form': form})
