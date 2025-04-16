from django.contrib.auth.models import User
from django.db import models

CURRENCY_CHOICES = (
    ('GBP', 'British Pound Sterling'),
    ('EUR', 'Euro'),
    ('USD', 'US Dollars')
)


class Money(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    money = models.IntegerField(default=750)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GBP')

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
