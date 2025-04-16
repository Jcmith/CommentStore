from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from transactions.models import Money
from decimal import Decimal
import requests


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
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
        fields = ("username", "first_name", "last_name", "currency", "email", "password1", "password2")

    def save(self, *args, **kwargs):
        # Save the user instance without immediately committing to the database
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save()

        # Set the baseline amount in GBP
        baseline_amount = 750
        chosen_currency = self.cleaned_data['currency']
        converted_amount = baseline_amount  # Default is baseline if no conversion is needed

        # Call the RESTful currency conversion web service
        if chosen_currency != 'GBP':
            conversion_url = f"http://localhost:8000/conversion/GBP/{chosen_currency}/{baseline_amount}/"
            try:
                response = requests.get(conversion_url, timeout=3)
                if response.status_code == 200:
                    conversion_data = response.json()
                    # Retrieve the converted amount from the response
                    converted_amount = float(conversion_data.get('converted_amount', baseline_amount))
                else:
                    converted_amount = baseline_amount
            except Exception as e:
                # In case of an exception, use the baseline amount
                converted_amount = baseline_amount

        # Create a Money record associated with this user using the converted amount
        Money.objects.create(
            name=user,
            money=Decimal(str(converted_amount)),
            currency=chosen_currency
        )
        return user
