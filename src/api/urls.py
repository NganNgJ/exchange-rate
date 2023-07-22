from django.urls import path
from api.views import (
    get_all_currency,
    create_currency,
    adjust_currency,
    get_all_exchange_rate,
    create_exchange_rate,
    calculate_exchange_rate,
    adjust_exchange_rate
)

urlpatterns = [
    # path('', apiOverview, name= 'apiOverview'),
    path('all-currencies/', get_all_currency),
    path('create-currency/', create_currency),
    path('adjust-currency/', adjust_currency),
    path('all-exchange-rate/', get_all_exchange_rate),
    path('create-exchange-rate/', create_exchange_rate),
    path('calculate-exchange-rate/', calculate_exchange_rate),
    path('adjust-exchange-rate/', adjust_exchange_rate),
 
]
