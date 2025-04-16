from decimal import Decimal

import requests
from django.contrib.auth.decorators import login_required
from django.db import transaction, OperationalError
from django.db.models import F
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from . import models
from transactions.forms import MoneyTransferForm
from .models import Money, Transaction
from django.contrib import messages
@login_required
def money_transfer(request):
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST, user=request.user)

        if form.is_valid():
            # Set payment source as the logged-in user and get other information from the form.
            src_user = request.user
            dst_username = form.cleaned_data["enter_destination_username"]
            money_to_transfer = form.cleaned_data["enter_money_to_transfer"]

            try:
                src_money = Money.objects.select_related().get(name=src_user)
                dst_money = Money.objects.select_related().get(name__username=dst_username)
                # Capture old balance
                old_balance = src_money.money
            except Money.DoesNotExist:
                messages.error(request, "One of the users does not exist.")
                return render(request, "transactions/moneytransfer.html", {"form": form})

            # Call the RESTful currency conversion web service
            converted_money_to_transfer = money_to_transfer
            if src_money.currency != dst_money.currency:
                conversion_url = f"http://localhost:8000/conversion/{src_money.currency}/{dst_money.currency}/{money_to_transfer}/"
                try:
                    response = requests.get(conversion_url, timeout=3)
                    if response.status_code == 200:

                        # Retrieve the converted amount from the response
                        conversion_data = response.json()
                        converted_money_to_transfer = Decimal(str(conversion_data.get("converted_amount", money_to_transfer)))
                    else:
                        converted_money_to_transfer = money_to_transfer
                except Exception as e:
                    # In case of an exception, use the original amount
                    converted_money_to_transfer = money_to_transfer
                    messages.warning(request,
                                     "Currency service unavailable rate.")

            try:
                with transaction.atomic():
                    # Deduct money from the source
                    src_money.money -= money_to_transfer
                    src_money.save()

                    # Add money to the destination
                    dst_money.money += converted_money_to_transfer
                    dst_money.save()

                    # Capture new balance
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
