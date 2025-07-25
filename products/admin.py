from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product

admin.site.register(Category, MPTTModelAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'avg_rating')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    # `specifications` maydonini tahrirlash sahifasiga qo'shamiz
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category')}),
        ('Asosiy ma\'lumotlar', {'fields': ('price', 'stock', 'description', 'image')}),
        ('Texnik xususiyatlar', {'fields': ('specifications',)}), # <-- YANGI BO'LIM
        ('Avtomatik maydonlar', {'fields': ('avg_rating',)}),
    )
    readonly_fields = ('avg_rating',)