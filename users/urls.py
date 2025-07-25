from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAccountViewSet, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register(r'account', UserAccountViewSet, basename='account')

urlpatterns = [
    # Router tomonidan yaratilgan URL'lar
    path('', include(router.urls)),
    
    # Alogida qolgan JWT manzillari
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]