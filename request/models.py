from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Request(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE, null=True, blank=True)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE, null=True, blank=True)
    request_time = models.DateTimeField('request time', default=timezone.now)
    request_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        details = ''
        details += f'From User     : {self.from_user}\n'
        details += f'To User       : {self.to_user}\n'
        details += f'Request Time  : {self.request_time}\n'
        details += f'Request Amount: {self.request_amount}\n'
        return details
