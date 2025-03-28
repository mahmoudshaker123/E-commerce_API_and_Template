from django.db import models
import random
import string
from store.models import Product
# Create your models here.

def generate_order_id(length=8):
    charcters = string.ascii_letters + string.digits
    return ''.join(random.choices(charcters, k=length))  




class Order(models.Model):
    order_id = models.CharField(max_length=8 , default=generate_order_id, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.PositiveIntegerField() 
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at',]),

        ]

    def __str__(self):
        return f"""Order {self.order_id}"""
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            unique_id = generate_order_id()
            while Order.objects.filter(order_id=unique_id).exists():
                unique_id = generate_order_id()
            self.order_id = unique_id

        super().save(*args, **kwargs)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity