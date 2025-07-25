from django.db.models.signals import post_save, post_delete
from django.db.models import Avg
from django.dispatch import receiver
from .models import Review

# @receiver dekoratori signalni funksiyaga bog'laydi.
# Bu funksiya Review modeli uchun 'save' yoki 'delete' amali bajarilgandan so'ng ishga tushadi.
@receiver([post_save, post_delete], sender=Review)
def update_product_average_rating(sender, instance, **kwargs):
    """
    Har bir sharh saqlanganda yoki o'chirilganda, tegishli mahsulotning 
    o'rtacha reytingini qayta hisoblab, yangilaydi.
    
    Args:
        sender: Signalni yuborgan model (Review).
        instance: Signalni ishga tushirgan obyekt (yangi sharh).
        **kwargs: Qo'shimcha argumentlar.
    """
    # Signalni ishga tushirgan sharhga tegishli bo'lgan mahsulotni olamiz
    product = instance.product
    
    # Shu mahsulotga tegishli barcha sharhlarning 'rating' maydoni bo'yicha
    # o'rtacha qiymatini hisoblaymiz.
    average = product.reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Agar natija None bo'lsa (mahsulotda umuman sharhlar qolmagan bo'lsa),
    # o'rtacha reytingni 0.0 ga tenglaymiz. Aks holda, hisoblangan qiymatni olamiz.
    product.avg_rating = average if average is not None else 0.0
    
    # Mahsulotning yangilangan o'rtacha reytingini ma'lumotlar bazasiga saqlaymiz.
    product.save()
