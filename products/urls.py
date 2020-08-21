from django.urls import path
from .views import HomeView, ProductView

app_name = 'products'

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('product/<slug>/', ProductView.as_view(), name='Product'),
]
