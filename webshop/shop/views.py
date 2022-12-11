from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages



from .models import ProductModel,CartItemModel,CartModel,OrderModel


class HomeListView(ListView):
    model=ProductModel
    template_name = 'shop/home.html'
    context_object_name = 'products'

class CartView(ListView):
    model=User
    template_name = 'shop/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
            user_id = self.request.user.id
            cart = CartModel.objects.get(user=user_id)
            data = CartItemModel.objects.filter(cart=cart.pk).select_related('product').all()
            return data

@login_required
def add_to_cart(request,product_id):
    product = get_object_or_404(ProductModel, pk=product_id)
    cart_qs = CartModel.objects.filter(user=request.user)
    
    
    if cart_qs.exists():
        cart = cart_qs[0]
        cart_item = CartItemModel.objects.filter(product=product)
       
        if cart_item.exists():
            cart_item_model = CartItemModel.objects.get(product=product)
            cart_item_model.quantity += 1
            # cart_item_model.total_price = cart_item_model.total_price.price*cart_item_model.quantity
            cart_item_model.save()
            messages.info(request,f"{product.product_name} has been added to your cart.")
            return(redirect('shop-home'))
            
        else:
            cart_item_model= CartItemModel.objects.create(product=product)
            cart_item_model.cart.add(cart)
            messages.info(request, f"{product.product_name} has been added to your cart.")
            return(redirect('shop-home'))
    else:
        cart = CartModel.objects.create(user=request.user)
        cart_item_model= CartItemModel.objects.create(product=product)
        cart_item_model.cart.add(cart)
        messages.info(request, f"{product.product_name} has been added to your cart.")
        return(redirect('shop-home'))

@login_required
def cart_remove(request,cart_item_id):
    cart_item = CartItemModel.objects.filter(id=cart_item_id).delete()
    return(redirect('cart-page'))

@login_required
def order(request):
    cart = CartModel.objects.filter(user=request.user)
    order = OrderModel.objects.create(user=request.user)
    order.cart.set(cart)
    cart.delete()
    return(redirect('shop-home'))

    
    