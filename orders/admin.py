from django.contrib import admin
from .models import Order , OrderItem
# Register your models here.


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'first_name', 'last_name', 'email', 'created_at', 'paid']
    inlines = [OrderItemAdmin]
