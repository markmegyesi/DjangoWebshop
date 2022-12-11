from django.db import models
from django.contrib.auth.models import User

class ProductModel(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'products'

    def __str__(self):
        return(f"{self.product_name}")

class CartModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    

    class Meta:
        db_table = 'cart'

    def __str__(self): 
        return self.user.username

class CartItemModel(models.Model):
    
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product')
    quantity = models.IntegerField(default=1)
    cart = models.ManyToManyField(CartModel)
    
    @property
    def total(self):
        return self.product.price * self.quantity
        

    class Meta:
        db_table = 'cart_items' 

    def __str__(self):
        return f'{self.quantity} of {self.product.product_name}'
    


class OrderModel (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart = models.ManyToManyField(CartModel)

    class Meta:
            db_table = 'orders'

def __str__(self): 
    return (f"{self.user}s order")  
