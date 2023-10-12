from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at', 'end_at', 'is_closed')
    list_filter = ('is_closed', 'user')


admin.site.register(Order, OrderAdmin)