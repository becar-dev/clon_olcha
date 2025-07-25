from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Obyektni faqat uning egasi o'zgartira olishini ta'minlovchi maxsus ruxsat.
    Boshqalar faqat o'qiy oladi.
    """
    def has_object_permission(self, request, view, obj):
        # O'qish uchun ruxsatlar (GET, HEAD, OPTIONS) hammaga beriladi.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Yozish uchun ruxsatlar faqat obyektning egasiga (author) beriladi.
        return obj.author == request.user