from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response # Faqat adminlar uchun ruxsat
from .serializers import UserSerializer, RegisterSerializer, UserDetailSerializer

# User modelini olishni unutmang
from django.contrib.auth import get_user_model
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    Foydalanuvchilarni ko'rish va tahrirlash uchun API endpoint.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # Dastlabki bosqichda faqat adminlar hamma foydalanuvchilarni ko'ra olsin.
    permission_classes = [AllowAny] 

class UserAccountViewSet(viewsets.ModelViewSet):
    """
    Foydalanuvchi hisobini boshqarish uchun ViewSet.
    - `create` (POST /account/): Har kim uchun ochiq ro'yxatdan o'tish.
    - `me` (GET/PUT /account/me/): Tizimga kirgan foydalanuvchi uchun o'z profilini boshqarish.
    - Qolgan barcha CRUD amallari (list, retrieve, update, destroy) faqat adminlar uchun.
    """
    queryset = User.objects.all().order_by('-id')

    def get_serializer_class(self):
        """Amalga qarab tegishli serializerni tanlaydi."""
        if self.action == 'create':
            return RegisterSerializer
        elif self.action == 'me':
            return UserDetailSerializer
        # 'me' va boshqa barcha amallar uchun ProfileSerializer ishlatiladi.
        return UserDetailSerializer



    def get_permissions(self):
        """Amalga qarab ruxsatlarni dinamik belgilaydi."""
        if self.action == 'create':
            # Har kim yangi akkaunt yarata oladi (ro'yxatdan o'tish).
            self.permission_classes = [AllowAny]
        elif self.action == 'me':
            # Faqat tizimga kirgan foydalanuvchi o'z profilini ko'ra oladi.
            self.permission_classes = [IsAuthenticated]
        else:
            # Qolgan barcha standart amallar (list, retrieve, update, destroy)
            # faqat administratorlar uchun ruxsat etilgan.
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request, *args, **kwargs):
        """
        Joriy foydalanuvchi profilini olish (GET) yoki yangilash (PUT/PATCH).
        Manzil: /api/v1/account/me/
        """
        instance = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        
        serializer = self.get_serializer(instance, data=request.data, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)