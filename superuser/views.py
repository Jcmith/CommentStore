from django.shortcuts import render, redirect
from transactions.models import Transaction
from .decorators import admin_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

# Admin home
@admin_required
def home(request):
    return render(request, 'superuser/admin_home.html')
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
def create_admin(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            staff_group = Group.objects.get(name='Administrators')
            user.groups.add(staff_group)
            return redirect('superuser:user_list')
    else:
        form = UserCreationForm()
    return render(request, 'superuser/create_admin.html', {'form': form})
