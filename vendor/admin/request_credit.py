from django.contrib import admin
from vendor.models import RequestCredit


@admin.register(RequestCredit)
class RequestCreditAdmin(admin.ModelAdmin):
    list_display = ("requester", "amount", "status", "created_at", "updated_at")
    search_fields = ("requester",)
    list_filter = ("status", "created_at", "updated_at")
