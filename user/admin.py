"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # 表示専用フィールドを指定
    readonly_fields = ('user_id',)

    # 管理画面に表示するフィールドのカスタマイズ
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'language', 'user_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'language'),
        }),
    )

# カスタムユーザーモデルを登録
admin.site.register(CustomUser, CustomUserAdmin)
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('user_name', 'mailaddress', 'language_code', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('user_name', 'mailaddress')
    ordering = ['user_name']  # 'username' を 'user_name' に修正
    fieldsets = (
        (None, {'fields': ('user_name', 'mailaddress', 'password')}),
        ('Personal info', {'fields': ('language_code',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'mailaddress', 'password1', 'password2', 'language_code'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

