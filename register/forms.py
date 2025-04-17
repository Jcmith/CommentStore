from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from transactions.models import Money
from decimal import Decimal
import requests

User = get_user_model()  # This ensures it uses register.CustomUser

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
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.currency = self.cleaned_data["currency"]  # Make sure this field exists on CustomUser
        user.save()

        # Set the baseline amount in GBP
        baseline_amount = 750
        chosen_currency = self.cleaned_data['currency']
        converted_amount = baseline_amount

        # Call REST API for conversion
        if chosen_currency != 'GBP':
            conversion_url = f"http://localhost:8000/conversion/GBP/{chosen_currency}/{baseline_amount}/"
            try:
                response = requests.get(conversion_url, timeout=3)
                if response.status_code == 200:
                    conversion_data = response.json()
                    converted_amount = float(conversion_data.get('converted_amount', baseline_amount))
            except Exception:
                converted_amount = baseline_amount

        # Create Money record
        Money.objects.create(
            name=user,
            money=Decimal(str(converted_amount)),
            currency=chosen_currency
        )

        return user
