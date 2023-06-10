from django.urls import path
from api.views import (
    get_tasks
)

urlpatterns = [
    # path('', apiOverview, name= 'apiOverview'),
    path('your-task/', get_tasks),
]
