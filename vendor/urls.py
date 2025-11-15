from django.urls import path, include
from rest_framework import routers

from vendor import views

router = routers.DefaultRouter()
router.register(r"vendor", views.VendorViewSet, basename="vendor")

urlpatterns = [
    path("", include(router.urls)),
]
