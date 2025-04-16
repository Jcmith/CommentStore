from django import forms
from . import models


class MoneyTransferForm(forms.ModelForm):
    class Meta:
        model = models.MoneyTransfer
        fields = ["enter_your_username", "enter_destination_username", "enter_money_to_transfer"]
