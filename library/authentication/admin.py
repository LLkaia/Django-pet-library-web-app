from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'email', 'is_superuser')
    list_filter = ('is_active', 'is_superuser', 'role')


admin.site.register(CustomUser, CustomUserAdmin)
