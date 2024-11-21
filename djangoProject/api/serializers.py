from rest_framework import serializers
from .models import CurrencyExchange


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrencyExchange
        fields = ['code']