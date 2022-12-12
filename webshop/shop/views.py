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
            cart = CartModel.objects.get(user=user_id, ordered=False)
            data = CartItemModel.objects.filter(cart=cart.pk).select_related('product').all()
            self.total_price=0
            for i in data:
                self.total_price+=i.total
            return data

    def get_context_data(self, **kwargs):
        
        context = super(CartView, self).get_context_data(**kwargs)
        context['total_price'] = self.total_price
        return context
    

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product = get_object_or_404(ProductModel, pk=request.POST.get('product'))
        print(product)
        quantity = request.POST.get('quantity')
        cart_qs = CartModel.objects.filter(user=request.user, ordered=False)
        print(quantity)

        if cart_qs.exists() and cart_qs.ordered == False:
            cart = cart_qs[0]
            cart_item = CartItemModel.objects.filter(product=product)

            if cart_item.exists():
                cart_item_model = CartItemModel.objects.get(product=product)
                cart_item_model.quantity += int(quantity)
                cart_item_model.save()
                messages.info(request,f"{product.product_name} has been added to your cart.")
                return(redirect('shop-home'))
                
            else:
                cart_item_model= CartItemModel.objects.create(product=product, quantity=quantity)
                cart_item_model.cart.add(cart)
                messages.info(request, f"{product.product_name} has been added to your cart.")
                return(redirect('shop-home'))
        else:
            cart = CartModel.objects.create(user=request.user)
            cart_item_model= CartItemModel.objects.create(product=product,quantity=quantity)
            cart_item_model.cart.add(cart)

        messages.info(request, f"{product.product_name} has been added to your cart.")
        return(redirect('shop-home'))



@login_required
def cart_exist(request):
    cart_qs = CartModel.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        return(redirect('cart-page'))
    else:
        messages.info(request, "You don't have a cart yet")
        return(redirect('shop-home'))

@login_required
def cart_remove(request,cart_item_id):
    cart_item = CartItemModel.objects.filter(id=cart_item_id).delete()
    return(redirect('cart-page'))

@login_required
def order(request):
    cart = CartModel.objects.get(user=request.user, ordered=False)
    cart_items = CartItemModel.objects.filter(cart=cart)
    for item in cart_items:
        product=ProductModel.objects.get(product_name=item)
        cart_item= CartItemModel.objects.get(product=product)
        order = OrderModel.objects.create(user=request.user, cart=cart, product=product,
                                         quantity=cart_item.quantity )
        order.save()
        product.quantity -= cart_item.quantity
        product.save()
    cart_items.delete()
    cart.ordered=True
    cart.save()
    return(redirect('receipt'))

@login_required
def direct_order(request, product_id): 
    product=ProductModel.objects.get(id=product_id)
    cart = CartModel.objects.create(user=request.user)
    quantity = request.POST.get('quantity')
    cart_item = CartItemModel.objects.create(product=product, quantity=quantity)
    cart_item.cart.add(cart)
    order = OrderModel.objects.create(user=request.user, cart=cart, product=product,
                                     quantity=cart_item.quantity )
    order.save()
    product.quantity-=cart_item.quantity
    product.save()
    cart_item.delete()
    cart.ordered=True
    cart.save()
    return(redirect('receipt'))

class RecieptListView(ListView):
    model=User
    template_name = 'shop/receipt.html'
    context_object_name = 'items'

    def get_queryset(self):
            user_id = self.request.user.id
            cart = CartModel.objects.latest('user')
            data = OrderModel.objects.filter(cart=cart).all()
            self.total_gross_price=0
            self.total_net_price=0
            for i in data:
                self.total_gross_price+=i.gross_price
                self.total_net_price+=i.net_price
            return data
            

    def get_context_data(self, **kwargs):
        
        context = super(RecieptListView, self).get_context_data(**kwargs)
        context['total_gross_price'] = self.total_gross_price
        context['total_net_price'] = self.total_net_price
        return context