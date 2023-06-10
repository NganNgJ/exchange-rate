from django.urls import path
from api.views import (
    get_all_currency,
    create_currency
)

urlpatterns = [
    # path('', apiOverview, name= 'apiOverview'),
    path('all-currencies/', get_all_currency),
    path('create-currency/', create_currency),
]
