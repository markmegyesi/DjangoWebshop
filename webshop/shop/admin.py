from django.contrib import admin
from .models import (ProductModel,CartModel,CartItemModel,OrderModel)

admin.site.register(ProductModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)
admin.site.register(OrderModel)