from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly # Maxsus ruxsatni import qilamiz

class ReviewViewSet(viewsets.ModelViewSet):
    # Har bir sharh uchun uning mahsuloti (product) va muallifini (author)
    # bitta so'rovda olish uchun `select_related` dan foydalanamiz.
    queryset = Review.objects.select_related('product', 'author').all()
    serializer_class = ReviewSerializer
    # Standart ruxsat: Tizimga kirmaganlar faqat o'qiy oladi.
    # Maxsus ruxsat: Faqat egasi o'zgartira oladi.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Yangi sharh yaratilganda, 'author' maydonini avtomatik ravishda
        # so'rov yuborgan foydalanuvchi bilan to'ldiradi.
        serializer.save(author=self.request.user)