import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('sepatu', 'Sepatu'),
        ('peralatan', 'Peralatan'),
        ('aksesoris', 'Aksesoris'),
        ('jaket', 'Jaket'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)
    price = models.IntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)

    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=20)
    sold = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    @property
    def is_product_best_seller(self):
        return self.sold > 40
        
    def increment_stock(self):
        self.stock += 1
        self.save()

    def decrement_stock(self):
        if self.stock > 0:
            self.stock -= 1
            self.save()