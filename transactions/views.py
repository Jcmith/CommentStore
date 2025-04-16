from django.db import transaction, OperationalError
from django.db.models import F
from django.shortcuts import render
from . import models
from transactions.forms import MoneyTransferForm
from .models import Money
from django.contrib import messages


# Create your views here.
def money_transfer(request):
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)

        if form.is_valid():

            src_username = form.cleaned_data["enter_your_username"]
            dst_username = form.cleaned_data["enter_destination_username"]
            money_to_transfer = form.cleaned_data["enter_money_to_transfer"]

            src_money = models.Money.objects.select_related().get(name__username=src_username)
            dst_money = models.Money.objects.select_related().get(name__username=dst_username)

            try:
                with transaction.atomic():
                    src_money.money = src_money.money - money_to_transfer
                    src_money.save()

                    dst_money.money = dst_money.money + money_to_transfer
                    dst_money.save()
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")

            # Money.objects.filter(name__username=src_username).update(money=F('money')-money_to_transfer)
            # Money.objects.filter(name__username=dst_username).update(money=F('money')+money_to_transfer)

        return render(request, "transactions/money.html", {"src_money": src_money, "dst_money": dst_money})

    else:
        form = MoneyTransferForm()

    return render(request, "transactions/moneytransfer.html", {"form": form})
