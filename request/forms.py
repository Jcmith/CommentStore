from django import forms
from django.contrib.auth.models import User


class InsertNewRequest(forms.Form):
    to_username = forms.CharField(label="Insert a username:", max_length=100)
    request_amount = forms.DecimalField(label="Insert the amount you want to request:", max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        # Pass the current user through the form context
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    # Check if the user is trying to send a request to themselves:
    def clean_to_username(self):
        name = self.cleaned_data.get("to_username")
        if self.user and name == self.user.username:
            raise forms.ValidationError("You cannot send a request to yourself!")
        try:
            user_obj = User.objects.get(username=name)
        except User.DoesNotExist:
            raise forms.ValidationError("No user with that username exists.")
        return user_obj
