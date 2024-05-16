from django.db import models

class InventoryImage(models.Model):
	image = models.ImageField(upload_to='images', blank=True, null=True)
	alt = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self) -> str:
		return str(self.alt)


class InventoryType(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ForeignKey(InventoryImage, on_delete=models.CASCADE, related_name="inventory_card_icon", null=True, blank=True)

    def __str__(self):
        return self.name




class Inventory(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    type = models.ForeignKey(InventoryType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
