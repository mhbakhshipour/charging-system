from django.contrib import admin
from customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "current_balance", "created_at", "updated_at")
    search_fields = ("phone_number",)
    list_filter = ("created_at", "updated_at")
