from django.contrib.auth.models import User
from django.db import models

CURRENCY_CHOICES = (
    ('GBP', 'British Pound Sterling'),
    ('EUR', 'Euro'),
    ('USD', 'US Dollars')
)


class Money(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=10, decimal_places=2, default=750)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GBP')

    CURRENCY_SYMBOLS = {
        'GBP': '£',
        'EUR': '€',
        'USD': '$',
    }

    @property
    def symbol(self):
        return self.CURRENCY_SYMBOLS.get(self.currency, '')

    @property
    def formatted(self):
        # format to two decimal places
        return f"{self.symbol}{self.money:.2f}"

    def __str__(self):
        details = ''
        details += f'Username     : {self.name}\n'
        details += f'Money       : {self.money}\n'
        details += f'Currency     : {self.currency}\n'
        return details


class MoneyTransfer(models.Model):
    enter_your_username = models.CharField(max_length=50)
    enter_destination_username = models.CharField(max_length=50)
    enter_money_to_transfer = models.IntegerField()

    def __str__(self):
        details = ''
        details += f'Your username            : {self.enter_your_username}\n'
        details += f'Destination username     : {self.enter_destination_username}\n'
        details += f'Money To Transfer         : {self.enter_money_to_transfer}\n'
        return details

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_time = models.DateTimeField(auto_now_add=True)
