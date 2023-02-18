from django.urls import path
from .views import bikes

urlpatterns = [
    path('', bikes, name='bikes'),
]
