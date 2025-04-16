from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from transactions import models
from transactions.models import Money


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    money = forms.IntegerField()
    currency = forms.ChoiceField(
        choices=[
            ('GBP', 'British Pound Sterling'),
            ('EUR', 'Euro'),
            ('USD', 'US Dollars')
        ],
        required=True,
        label="Currency"
    )


    class Meta:
        model = User
        fields = ("username", "money", "first_name", "last_name", "currency", "email", "password1", "password2")

    def save(self, *args, **kwargs):
        # Save the user instance without immediately committing to the database
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save()
        # Create a Money record associated with this user
        Money.objects.create(
            name=user,
            money=self.cleaned_data['money'],
            currency=self.cleaned_data['currency']
        )
        return user




