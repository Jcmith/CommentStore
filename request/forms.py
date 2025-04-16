from django import forms


class InsertNewRequest(forms.Form):
    name = forms.CharField(label="Insert a username:", max_length=100)
    request_amount = forms.CharField(label="Insert the amount you want to request:", max_length=8)
