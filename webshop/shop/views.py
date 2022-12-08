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
    print(cart_qs)
    cart_item = CartItemModel.objects.get_or_create(cart=cart_qs[0])
    
    print (cart_item)
    if cart_qs.exists():
        cart = cart_qs[0]
        print(cart.product_id)
        if cart.product == product_id:
            cart_item.quantity += request.POST.get('select')
            cart_item.product.save()
            messages.info(request,f"{product.product_name} has been added to your cart.")
            return(redirect('shop-home'))
            
        else:
            cart.cart.add(cart_item)
            messages.info(request, f"{product.product_name} has been added to your cart.")
            return(redirect('shop-home'))
    else:
        cart = CartModel.objects.create(user=request.user)
        cart.cart.add(cart_item)
        messages.info(request, f"{product.product_name} has been added to your cart.")
        return(redirect('shop-home'))
