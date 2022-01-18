from django.db import models

class CurrencyRate(models.Model):
    brl = models.DecimalField(max_digits=17, decimal_places=10)
    eur = models.DecimalField(max_digits=17, decimal_places=10)
    jpy = models.DecimalField(max_digits=17, decimal_places=10)
    date = models.DateField(unique=True)