from django import forms


class InsertNewComment(forms.Form):
    name = forms.CharField(label="Insert a name:", max_length=100)
    payment_amount = forms.CharField(label="Insert a payment amount:", max_length=8)
