from django.urls import path
from .views import seia

urlpatterns = [
    path('', seia, name='seia'),
]
