from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from transactions.models import Transaction, Money
from .decorators import admin_required
from .forms import CustomUserCreationForm

User = get_user_model()

# Admin home
@admin_required
def superuser_home(request):
    return render(request, 'superuser/superuser_home.html')

# Lists all users
@admin_required
def user_list(request):
    users = User.objects.all()
    user_data = []

    for user in users:
        try:
            money = Money.objects.get(name=user)
            balance = money.formatted  # formatted = £750.00, etc.
            currency = money.currency
        except Money.DoesNotExist:
            balance = 'N/A'
            currency = 'N/A'

        user_data.append({
            'username': user.username,
            'full_name': user.get_full_name(),
            'email': user.email,
            'balance': balance,
            'currency': currency,
        })

    return render(request, 'superuser/user_list.html', {'users': user_data})

# Lists all transactions
@admin_required
def transaction_list(request):
    txs = Transaction.objects.select_related('sender', 'receiver')
    updated_txs = []

    for tx in txs:
        # Get sender's currency symbol
        try:
            sender_money = Money.objects.get(name=tx.sender)
            sender_symbol = sender_money.symbol
        except Money.DoesNotExist:
            sender_symbol = ''

        # Get receiver's currency symbol
        try:
            receiver_money = Money.objects.get(name=tx.receiver)
            receiver_symbol = receiver_money.symbol
        except Money.DoesNotExist:
            receiver_symbol = ''

        updated_txs.append({
            'time': tx.transaction_time,
            'sender': tx.sender.username,
            'receiver': tx.receiver.username,
            'amount': tx.amount,
            'converted_amount': tx.converted_amount,
            'sender_symbol': sender_symbol,
            'receiver_symbol': receiver_symbol,
        })

    return render(request, 'superuser/transaction_list.html', {'txs': updated_txs})

# Register new Admin
@admin_required
def create_superuser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True  # promote to admin
            user.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'superuser/create_superuser.html', {'form': form})
