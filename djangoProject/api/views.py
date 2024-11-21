from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CurrencyExchange
from .serializers import CurrencySerializer
from django.shortcuts import get_object_or_404
# Create your views here.

@api_view(['GET'])
def CurrencyViewSet(request):
    queryset = CurrencyExchange.objects.all()
    serializer = CurrencySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ExchangeViewSet(request, base_currency, sub_currency):
    base = CurrencyExchange.objects.filter(code=base_currency.upper()).first()
    sub = CurrencyExchange.objects.filter(code=sub_currency.upper()).first()
    if not base:
        return Response(f"{base_currency} code is not exists", status=status.HTTP_400_BAD_REQUEST)
    elif not sub:
        return Response(f"{sub_currency} code is not exists", status=status.HTTP_400_BAD_REQUEST)

    return Response({f"currency_pair": f"{base.code}{sub.code}", "exchange_rate":round(sub.usdRate/base.usdRate, 4)})