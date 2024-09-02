
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django App Interview Task Backend APIs",
        default_version='v1',
        description=(
            "This is the API documentation for Django App Interview Task project APIs.\n\n"
            "Contacts:\n"
            "- Ali Sina Sultani: alisinasultani@gmail.com\n"
        ),
        contact=openapi.Contact(email="alisinasultani@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path("__reload__/", include("django_browser_reload.urls")),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = "Django App Interview Task"
admin.site.site_title = "Django App Interview Task"
admin.site.index_title = "Django App Interview Task"