from django.urls import path
from .views import HomeListView,CartView,add_to_cart



urlpatterns = [
    path('', HomeListView.as_view(), name="shop-home"),
    path('cart/<int:product_id>', add_to_cart, name='cart'),
    path('cart/', CartView.as_view(), name='cart-page'),
]