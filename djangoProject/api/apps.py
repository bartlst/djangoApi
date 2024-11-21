import requests
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        post_migrate.connect(run_initialization_script, sender=self)

def run_initialization_script(sender, **kwargs):
    from .models import CurrencyExchange
    import freecurrencyapi
    from django.conf import settings

    
    API_KEY = settings.FREECURRENCYAPI_KEY
    if not API_KEY:
        print("Error: Lack of API key. Make sure that API key is located inside of .env.local file.")
        return

    client = freecurrencyapi.Client(API_KEY)

    try:
        print(client)
        result = client.latest()
        
        if 'data' in result:
            for code, rate in result['data'].items():
                CurrencyExchange.objects.update_or_create(
                    code=code,
                    defaults={
                        'usdRate': round(rate,4),  
                    }
                )
            print("Initial data has been added to database.")
        else:
            print("Lack of data attribute in API response.")
    except Exception as e:
        print(f"Exception occurred while collecting data from API: {e}")
