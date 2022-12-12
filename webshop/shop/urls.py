from django.urls import path
from .views import HomeListView,CartView,add_to_cart,cart_remove,order,cart_exist,direct_order



urlpatterns = [
    path('', HomeListView.as_view(), name="shop-home"),
    path('cart/add/', add_to_cart, name='cart'),
    path('cart/', CartView.as_view(), name='cart-page'),
    path('cart/remove/<int:cart_item_id>', cart_remove, name='remove'),
    path('cart/order/', order, name='order'),
    path('cart/exist/',cart_exist , name='exist'),
    path('order/<int:product_id>',direct_order , name='order'),
]