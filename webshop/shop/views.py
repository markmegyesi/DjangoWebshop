from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect


from .models import ProductModel,CartItemModel,CartModel


class HomeListView(ListView):
    model=ProductModel
    template_name = 'shop/home.html'
    context_object_name = 'products'

class CartView(ListView):
    model=CartItemModel
    template_name = 'shop/cart.html'
    context_object_name = 'items'

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
