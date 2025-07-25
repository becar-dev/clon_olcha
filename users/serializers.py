from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile

User = get_user_model() # settings.py da belgilangan AUTH_USER_MODEL ni oladi

class UserSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi ma'lumotlarini JSON formatiga o'tkazish uchun serializer.
    """
    class Meta:
        model = User
        # API orqali ko'rsatiladigan va qabul qilinadigan maydonlar
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        # Parolni faqat yozish uchun (write_only) qilamiz, ya'ni GET so'rovlarida ko'rinmaydi.
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        """
        Yangi foydalanuvchi yaratilganda parolni to'g'ri hash'lash (shifrlash) uchun.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) # Parolni shifrlaydi
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Foydalanuvchi ma'lumotlari yangilanganda parolni to'g'ri hash'lash uchun.
        """
        # Agar so'rovda parol kelsa, uni yangilaymiz
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        # Qolgan maydonlarni standart usulda yangilaymiz
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    """Faqat UserProfile ma'lumotlari uchun"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'birth_date']

class UserDetailSerializer(serializers.ModelSerializer):
    """Foydalanuvchining to'liq ma'lumotlarini ko'rsatish uchun"""
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image', 'phone_number', 'profile']