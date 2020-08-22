from django.contrib import admin
from src.models.product import Item
from src.models.orders import OrderItem, Order

# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Item)
