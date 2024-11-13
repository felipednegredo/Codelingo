from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'Nome', 'Email', 'is_professor', 'is_aluno', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('Nome', 'Email', 'Matricula')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'Nome', 'Email', 'password1', 'password2', 'is_professor', 'is_aluno', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('username', 'Nome', 'Email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)