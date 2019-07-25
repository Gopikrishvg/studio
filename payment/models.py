from django.db import models
from django.conf import Settings


class Payment(models.Model):
    amount = models.FloatField()
    type_of_payment = models.CharField()
    transaction_id = models.CharField(max_length=20)
    date_of_payment = models.DateField(auto_now=True)
    user = models.ForeignKey(Settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
