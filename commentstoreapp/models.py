from django.db import models

class Payment(models.Model):
    name = models.CharField(max_length=100)
    payment_time = models.DateTimeField('payment time')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        details = ''
        details += f'Name          : {self.name}\n'
        details += f'Payment Time  : {self.payment_time}\n'
        details += f'Payment Amount: {self.payment_amount}\n'
        return details
