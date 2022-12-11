from django.urls import path
from .views import HomeListView,CartView,add_to_cart,cart_remove,order,cart_exist



urlpatterns = [
    path('', HomeListView.as_view(), name="shop-home"),
    path('cart/<int:product_id>', add_to_cart, name='cart'),
    path('cart/', CartView.as_view(), name='cart-page'),
    path('cart/remove/<int:cart_item_id>', cart_remove, name='remove'),
    path('cart/order/', order, name='order'),
    path('cart/exist/',cart_exist , name='exist'),
]