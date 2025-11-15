from django.urls import path, include
from rest_framework import routers

from customer import views

router = routers.DefaultRouter()
router.register(r"customer", views.CustomerViewSet, basename="customer")

urlpatterns = [
    path("", include(router.urls)),
]
