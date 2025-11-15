from django.contrib import admin
from vendor.models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "current_balance", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
