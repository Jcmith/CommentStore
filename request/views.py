from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.timezone import now, localtime
from request.forms import InsertNewRequest
from request.models import Request
from transactions.models import Money


@csrf_protect
def commentstore(request):
    if request.method == 'POST':
        form = InsertNewRequest(request.POST)
        d = localtime(now())

        if form.is_valid():
            n = form.cleaned_data["name"]
            c = form.cleaned_data["request_amount"]
            t = Request(name=n, request_time=d, request_amount=c)
            t.save()

            # Retrieve the current list of requests:
            cmnt_list = list(Request.objects.all())
            return render(request, "request/home.html", {"cmnt_list": cmnt_list})
    else:
        form = InsertNewRequest()

    return render(request, "request/request.html", {"form": form})
@csrf_protect
def home(request):
    # Get the current list of requests directly from the model:
    cmnt_list = list(Request.objects.all())
    return render(request, "request/home.html", {"cmnt_list": cmnt_list})
