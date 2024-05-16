from django.urls import path
from .views import DashboardInventoryView


urlpatterns = [
    path("inventory/", DashboardInventoryView.as_view(), name="inventory"),

]
