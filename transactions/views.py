from decimal import Decimal
import requests
from django.contrib.auth.decorators import login_required
from django.db import transaction, OperationalError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Money, Transaction
from transactions.forms import MoneyTransferForm
from django.contrib import messages

@login_required
def money_transfer(request):
    old_balance = None
    new_balance = None
    dst_username = None
    money_to_transfer = None

    if request.method == 'POST':
        form = MoneyTransferForm(request.POST, user=request.user)

        if form.is_valid():
            src_user = request.user
            dst_username = form.cleaned_data["enter_destination_username"]
            money_to_transfer = form.cleaned_data["enter_money_to_transfer"]

            try:
                src_money = Money.objects.select_related().get(name=src_user)
                dst_money = Money.objects.select_related().get(name__username=dst_username)
                old_balance = src_money.money
            except Money.DoesNotExist:
                messages.error(request, "User does not exist.")
                return render(request, "transactions/moneytransfer.html", {"form": form})

            # Currency conversion logic
            converted_money_to_transfer = money_to_transfer
            if src_money.currency != dst_money.currency:
                conversion_url = f"http://localhost:8000/conversion/{src_money.currency}/{dst_money.currency}/{money_to_transfer}/"
                try:
                    response = requests.get(conversion_url, timeout=3)
                    if response.status_code == 200:
                        conversion_data = response.json()
                        converted_money_to_transfer = Decimal(str(conversion_data.get("converted_amount", money_to_transfer)))
                except Exception:
                    messages.warning(request, "Currency service unavailable. Using original amount.")

            try:
                with transaction.atomic():
                    src_money.money -= money_to_transfer
                    src_money.save()

                    dst_money.money += converted_money_to_transfer
                    dst_money.save()

                    new_balance = src_money.money
            except OperationalError:
                messages.info(request, "Transfer operation is not possible now.")
                return render(request, "transactions/moneytransfer.html", {"form": form})

            # Log the transaction
            Transaction.objects.create(
                sender=src_money.name,
                receiver=dst_money.name,
                amount=money_to_transfer,
                converted_amount=converted_money_to_transfer,
            )

            return render(request, "transactions/transaction_success.html", {
                "old_balance": old_balance,
                "amount": money_to_transfer,
                "dst_username": dst_username,
                "new_balance": new_balance,
                "symbol": src_money.symbol,
            })

    else:
        form = MoneyTransferForm()

    return render(request, "transactions/moneytransfer.html", {"form": form})
