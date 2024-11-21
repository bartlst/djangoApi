from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse, resolve 
from .models import CurrencyExchange
from .views import CurrencyViewSet, ExchangeViewSet 


class CurrencyEndpointTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.currency_usd = CurrencyExchange.objects.create(code='DEF', usdRate=1.0)
        self.currency_eur = CurrencyExchange.objects.create(code='ET1', usdRate=0.85)
        self.currency_gbp = CurrencyExchange.objects.create(code='ET2', usdRate=0.75)

        self.currency_list_url = reverse('currency-list') 


    def test_exchange_view_set_valid(self):
        url = reverse('exchange-rate', args=['DEF', 'ET1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['currency_pair'], 'DEFET1')
        self.assertEqual(response.data['exchange_rate'], round(0.85 / 1.0, 4)) 


    def test_exchange_view_set_invalid_base_currency(self):
        url = reverse('exchange-rate', args=['XXX', 'ET1']) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "XXX code is not exists")

    
    def test_exchange_view_set_invalid_sub_currency(self):
        url = reverse('exchange-rate', args=['DEF', 'YYY'])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "YYY code is not exists")

    
    def test_currency_view_set_empty(self):
        CurrencyExchange.objects.all().delete()  
        response = self.client.get(self.currency_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])  

