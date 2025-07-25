# Biz Django'ning barcha autentifikatsiya imkoniyatlariga ega bo'lgan,
# ammo o'zimiz qo'shimcha maydonlar qo'sha oladigan yangi model yaratamiz.

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey

class CustomUser(AbstractUser):
    """
    Django'ning standart User modelini kengaytiruvchi model.
    Kelajakda bu yerga telefon raqami, manzil, profil rasmi kabi
    maydonlarni qo'shishimiz mumkin.
    """
    
    image = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name="User rasmi")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    # Har bir profil bitta foydalanuvchiga tegishli bo'ladi (One-to-One)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, verbose_name="O'zi haqida")
    # Rasm yuklash uchun Pillow kutubxonasi kerak bo'ladi (pip install Pillow)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Avatar")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    
    class Meta:
        verbose_name = "Foydalanuvchi Profili"
        verbose_name_plural = "Foydalanuvchi Profillari"

    def __str__(self):
        return f"{self.user.username} profili"