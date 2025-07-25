from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
import random
import string

def generate_unique_slug(klass, field):
    """
    Bir xil slug'lar yaratilishining oldini olish uchun noyob slug generatsiya qiladi.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    # Tasodifiy harflar va raqamlar qo'shish uchun
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    
    # Agar bunday slug mavjud bo'lsa, oxiriga tasodifiy belgilar qo'shamiz
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{origin_slug}-{random_suffix}'
    return unique_slug


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Kategoriya nomi")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug (URL)")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Kategoriya rasmi") 
    

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        # Agar slug bo'sh bo'lsa, uni noyob qilib yaratamiz
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug (URL)")
    description = models.TextField(blank=True, verbose_name="Tavsifi")
    specifications = models.JSONField(
        blank=True, 
        null=True, 
        verbose_name="Texnik xususiyatlari"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    stock = models.PositiveIntegerField(default=0, verbose_name="Ombordagi soni")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Mahsulot rasmi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avg_rating = models.FloatField(default=0.0, verbose_name="O'rtacha reyting")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name