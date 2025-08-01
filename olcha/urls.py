from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view endi ancha sodda ko'rinishda, chunki sozlamalar settings.py da
schema_view = get_schema_view(
   openapi.Info(
      title="Olcha.uz Clone API",
      default_version='v1',
      description="Olcha.uz sayti uchun yaratilgan API dokumentatsiyasi.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Bizning API manzillarimiz
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('reviews.urls')),
    
    # Swagger va ReDoc uchun URL manzillari
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)