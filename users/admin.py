
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile # UserProfile'ni import qilamiz

# UserProfile'ni CustomUser admin sahifasiga ichki (inline) qilib qo'shamiz
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'image', 'phone_number')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'image', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'image', 'phone_number')}),
    )

# Eski register'ni o'chirib, yangisini yozamiz
# XATO TUZATILDI: unregister faqat bitta argument (model) qabul qiladi.
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass
admin.site.register(CustomUser, CustomUserAdmin)