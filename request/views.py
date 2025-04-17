from decimal import Decimal

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.timezone import now, localtime
from request.forms import InsertNewRequest
from request.models import Request
from transactions.models import Money, Transaction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


@login_required
def new_request(request):
        form = InsertNewRequest(request.POST or None, user=request.user)

        if request.method == 'POST':
            if form.is_valid():
                # save the new payment-request
                to_user = form.cleaned_data["to_username"]
                request_amount = form.cleaned_data["request_amount"]
                timestamp = localtime(now())

                Request.objects.create(
                    from_user=request.user,
                    to_user=to_user,
                    request_time=timestamp,
                    request_amount=request_amount
                )
                return redirect('home')

        # for GET, or POST with invalid data, render the form
        return render(request, "request/request.html", {"form": form})


@login_required
def home(request):
    # Get current balance
    try:
        user_money = Money.objects.get(name=request.user)
    except Money.DoesNotExist:
        user_money = None

    # Get all payment requests and convert them
    raw_reqs = Request.objects.filter(to_user=request.user)
    display_requests = []
    for r in raw_reqs:
        req_money = Money.objects.get(name=r.from_user)
        amt = r.request_amount
        if req_money.currency != user_money.currency:
            url = (
                f"http://localhost:8000/conversion/"
                f"{req_money.currency}/"
                f"{user_money.currency}/"
                f"{amt}/"
            )
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                amt = Decimal(str(data.get("converted_amount", amt)))
        display_requests.append({
            "from": r.from_user.username,
            "time": r.request_time,
            "amount": amt,
            "symbol": user_money.symbol,
        })

    # Get all transactions
    user_transactions = Transaction.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-transaction_time')

    context = {
        "user_money": user_money,
        "display_requests": display_requests,
        "transactions": user_transactions,
    }
    return render(request, "request/home.html", context)
