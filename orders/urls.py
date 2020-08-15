from django.urls import path
from .views import HomeView, Checkout, ProductView, add_to_cart, remove_from_cart

app_name = 'orders'

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('product/<slug>/', ProductView.as_view(), name='Product'),
    path('checkout', Checkout, name='Checkout'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
]
