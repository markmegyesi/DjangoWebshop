from django.contrib import admin
from .models import (ProductModel,CartModel,CartItemModel)

admin.site.register(ProductModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)