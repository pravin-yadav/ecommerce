from django.urls import path
from .views import Checkout, add_to_cart, remove_from_cart, OrderSummary, remove_quantity_from_cart, add_quantity_in_cart

app_name = 'orders'

urlpatterns = [
    path('checkout/', Checkout, name='Checkout'),
    path('order-summary/', OrderSummary.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('add-quantity-in-cart/<slug>/', add_quantity_in_cart,
         name='add-quantity-in-cart'),
    path('remove-quantity-from-cart/<slug>/',
         remove_quantity_from_cart, name='remove-quantity-from-cart'),
]
