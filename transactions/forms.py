from django import forms
from . import models


class MoneyTransferForm(forms.ModelForm):
    class Meta:
        model = models.MoneyTransfer
        fields = ["enter_destination_username", "enter_money_to_transfer"]


    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    # Prevent self-transfer:
    def clean_enter_destination_username(self):
        dst = self.cleaned_data["enter_destination_username"]
        if dst == self.user.username:
            raise forms.ValidationError("You cannot transfer money to yourself.")
        return dst
