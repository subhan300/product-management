from django.contrib import admin
from .models import Inventory, InventoryType, InventoryImage

admin.site.register(InventoryType)
admin.site.register(Inventory)
admin.site.register(InventoryImage)