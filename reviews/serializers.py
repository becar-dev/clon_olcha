from rest_framework import serializers
from .models import Review
from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    # `rating` maydonini aniq belgilab, unga validator qo'shamiz.
    # Bu modeldagi validatorni takrorlasa-da, API javoblarini chiroyli qiladi.
    rating = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        help_text="Reyting 1 dan 5 gacha bo'lishi kerak."
    )

    class Meta:
        model = Review
        fields = ['id', 'product', 'author', 'text', 'rating', 'created_at']
        extra_kwargs = {'product': {'write_only': True}}