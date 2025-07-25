from rest_framework import serializers
from .models import Category, Product

class SimpleCategorySerializer(serializers.ModelSerializer):
    """Mahsulotlar ichida kategoriyani oddiy ko'rsatish uchun"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Bitta kategoriyaning detalini ko'rsatish uchun (bolalari bilan)"""
    children = SimpleCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children', 'image']
        read_only_fields = ['slug']


class ProductSerializer(serializers.ModelSerializer):
    # Endi ProductSerializer oddiy kategoriya serializeridan foydalanadi
    category = SimpleCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Product
        # `slug` (faqat o'qish uchun) va `image` maydonlarini qo'shamiz
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'category', 'category_id', 'image', 'avg_rating', 'specifications']
        read_only_fields = ['slug', 'avg_rating']
