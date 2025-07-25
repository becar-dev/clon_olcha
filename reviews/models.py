from django.db import models
from django.conf import settings
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name="Sharh matni")
    rating = models.PositiveSmallIntegerField(
        default=5, 
        verbose_name="Reyting (1-5)",
        validators=[
            MinValueValidator(1, message="Reyting 1 dan kam bo'lishi mumkin emas."),
            MaxValueValidator(5, message="Reyting 5 dan ko'p bo'lishi mumkin emas.")
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        # Bir foydalanuvchi bitta mahsulotga faqat bitta sharh qoldira oladi
        unique_together = ('product', 'author')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} dan {self.product.name} uchun sharh"