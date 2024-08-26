
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    
]
