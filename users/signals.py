from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

# @receiver dekoratori signalni funksiyaga bog'laydi.
# post_save - bu signal 'save' metodi chaqirilgandan keyin ishga tushadi.
# sender=settings.AUTH_USER_MODEL - faqat CustomUser modeli saqlanganda ishga tushadi.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Yangi foydalanuvchi yaratilganda (created=True), unga tegishli
    UserProfile obyektini avtomatik ravishda yaratadi.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Foydalanuvchi ma'lumotlari saqlanganda, uning profilini ham saqlaydi.
    """
    instance.profile.save()