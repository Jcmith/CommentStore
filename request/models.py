from django.db import models
from django.utils import timezone


class Request(models.Model):
    name = models.CharField(max_length=100)
    request_time = models.DateTimeField('request time', default=timezone.now)
    request_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        details = ''
        details += f'Name          : {self.name}\n'
        details += f'Request Time  : {self.request_time}\n'
        details += f'Request Amount: {self.request_amount}\n'
        return details
