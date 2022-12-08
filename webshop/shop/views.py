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
    # if request.method == 'POST':
    
    product = get_object_or_404(ProductModel, pk=product_id)
    cart_qs = CartModel.objects.filter(user=request.user)
    
    
    if cart_qs.exists():
        cart = cart_qs[0]
        cart_item = CartItemModel.objects.get_or_create(product=product)
        print(cart_item[0])
        # cart_item =CartItemModel(product=product)
        # cart_item.save()
        # cart_item.cart.add(cart)
        # cart_item.save()
        print (cart_item)
        if cart_item.product == product_id:
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request,f"{product.product_name} has been added to your cart.")
            return(redirect('shop-home'))
            
        # else:
        #     cart_item.cart.add(cart_item)
        #     messages.info(request, f"{product.product_name} has been added to your cart.")
        #     return(redirect('shop-home'))
    else:
        cart = CartModel.objects.create(user=request.user)
        cart_item_model= CartItemModel.objects.create(cart=cart)
        cart_item_model.cart.add(cart)
        messages.info(request, f"{product.product_name} has been added to your cart.")
        return(redirect('shop-home'))
