from django.contrib import admin

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "created_at", "is_valid"]
    list_filter = ["product", "user", "created_at", "is_valid"]
