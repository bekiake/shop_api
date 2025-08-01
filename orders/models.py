from django.db import models
from django.conf import settings
from products.models import Product
# Create your models here.

class Order(models.Model):
    
    STATUS_CHOICES = [
        ('processing', 'Qayta ishlanmoqda'),
        ('shipped', 'Jo\'natildi'),
        ('delivered', 'Yetkazildi'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Buyurtma #{self.id} {self.user.email}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} {self.quantity}x"