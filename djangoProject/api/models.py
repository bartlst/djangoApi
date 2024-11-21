from django.db import models
from django.contrib import admin
from django.utils.html import format_html

# Create your models here.


class CurrencyExchange(models.Model):
    code = models.CharField(max_length=30, blank=False, null=False)
    usdRate = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.code}"