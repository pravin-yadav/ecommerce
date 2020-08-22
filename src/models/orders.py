from django.db import models
from django.conf import settings
from src.models.product import Item

# Create your models here.


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved_on_item(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_item_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_item_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_final_price()
        return total

    def get_item_total_discount_price(self):
        discount_price = 0
        for order_item in self.items.all():
            if order_item.item.discount_price:
                discount_price += (order_item.get_total_item_price() -
                                   order_item.get_total_item_discount_price())
        return discount_price
