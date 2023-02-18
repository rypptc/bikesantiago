from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bikes/', include('bikes_info.urls'), name='bikes-info'),
    path('seia/', include('seia.urls'), name='seia')
]
