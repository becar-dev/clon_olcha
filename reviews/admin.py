

from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin panelida Sharhlar (Reviews) modelini boshqarish uchun sozlamalar.
    """
    # Ro'yxatda ko'rinadigan ustunlar
    list_display = ('product', 'author', 'rating', 'created_at')
    
    # O'ng tomonda paydo bo'ladigan filtr paneli
    list_filter = ('rating', 'created_at')
    
    # Qidiruv maydoni qaysi ustunlar bo'yicha ishlashi
    search_fields = ('text', 'product__name', 'author__username')
    
    # Faqat o'qish uchun mo'ljallangan maydonlar (tahrirlab bo'lmaydi)
    readonly_fields = ('created_at',)

    # Tahrirlash sahifasidagi maydonlar tartibi
    fieldsets = (
        (None, {
            'fields': ('product', 'author')
        }),
        ('Sharh ma\'lumotlari', {
            'fields': ('text', 'rating', 'created_at')
        }),
    )
