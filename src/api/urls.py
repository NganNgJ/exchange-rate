from django.urls import path
from api import views
from api.views import (
    index
)

urlpatterns = [
    # path('', apiOverview, name= 'apiOverview'),
    path('your-task/', views.index, name='your-task'),
]