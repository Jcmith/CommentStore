from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.timezone import now, localtime
from commentstoreapp.forms import InsertNewComment
from commentstoreapp.models import Payment

@csrf_protect
def commentstore(request):
    if request.method == 'POST':
        form = InsertNewComment(request.POST)
        d = localtime(now())

        if form.is_valid():
            n = form.cleaned_data["name"]
            c = form.cleaned_data["payment_amount"]
            t = Payment(name=n, payment_time=d, payment_amount=c)
            t.save()

            # Retrieve the current list of payments:
            cmnt_list = list(Payment.objects.all())
            return render(request, "commentstoreapp/home.html", {"cmnt_list": cmnt_list})
    else:
        form = InsertNewComment()

    return render(request, "commentstoreapp/comment.html", {"form": form})
@csrf_protect
def home(request):
    # Get the current list of payments directly from the model:
    cmnt_list = list(Payment.objects.all())
    return render(request, "commentstoreapp/home.html", {"cmnt_list": cmnt_list})
