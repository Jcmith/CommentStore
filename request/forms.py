from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class InsertNewRequest(forms.Form):
    to_username = forms.CharField(label="Insert a username:", max_length=100)
    request_amount = forms.DecimalField(
        label="Insert the amount you want to request:",
        max_digits=10,
        decimal_places=2
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # current logged-in user
        super().__init__(*args, **kwargs)

    def clean_to_username(self):
        name = self.cleaned_data.get("to_username")
        if self.user and name == self.user.username:
            raise forms.ValidationError("You cannot send a request to yourself!")
        try:
            user_obj = User.objects.get(username=name)
        except User.DoesNotExist:
            raise forms.ValidationError("No user with that username exists.")
        return user_obj  # return the actual user object for use in views
