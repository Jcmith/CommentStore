from django.http import HttpResponse
from django.shortcuts import render
from commentstoreapp.commentstore import CommentStore
from commentstoreapp.forms import InsertNewComment
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

store = CommentStore()
cmnt_list = []


@csrf_exempt
def commentstore(request):

    if request.method == 'POST':
        form = InsertNewComment(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            c = form.cleaned_data["comment_str"]
            d = form.cleaned_data["visit_date"]
            store.insertcomment(n, d, c)
        cmnt_list = list(store.commentlist.queue)

        return render(request, "commentstoreapp/home.html", {'cmnt_list': cmnt_list})
    else:
        form = InsertNewComment()

    return render(request, "commentstoreapp/comment.html", {"form": form})


def home(request):
    return render(request, "commentstoreapp/home.html", {'cmnt_list': cmnt_list})
