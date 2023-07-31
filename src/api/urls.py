from rest_framework import routers
from django.urls import path, include
from api.views import (
    CurrencyViewSet,
    ExchangerateHistoryViewset,
    ExchangerateViewset,
    get_all_currency,
    create_currency,
    adjust_currency,
    get_all_exchange_rate,
    create_exchange_rate,
    calculate_exchange_rate,
    adjust_exchange_rate
)

router = routers.DefaultRouter()
router.register(r'currencies', CurrencyViewSet)
router.register(r'exchangerate-histories',ExchangerateHistoryViewset)
router.register(r'exchangerates',ExchangerateViewset)

urlpatterns = [
    path('', include(router.urls)),
    # path('', apiOverview, name= 'apiOverview'),
    path('all-currencies/', get_all_currency),
    path('create-currency/', create_currency),
    path('adjust-currency/', adjust_currency),
    path('all-exchange-rate/', get_all_exchange_rate),
    path('create-exchange-rate/', create_exchange_rate),
    path('calculate-exchange-rate/', calculate_exchange_rate),
    path('adjust-exchange-rate/', adjust_exchange_rate),
 
]
