from django.db import models
from django.shortcuts import reverse

# Create your models here.
CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sportwear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    thumbnail = models.ImageField(
        default="https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/12.jpg", blank=True, null=True)
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=2, default="Shirt")
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=1, default="primary")
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("ecommerce:Product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("ecommerce:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("ecommerce:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.title
