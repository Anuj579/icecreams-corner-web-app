from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)  
    email = models.EmailField(max_length=120)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date= models.DateField()

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name= models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class IceCream(models.Model):
    name = models.CharField(max_length=100)
    volume = models.CharField(max_length=20)  # e.g., "100ml", "250ml"
    price = models.FloatField()
    image= models.ImageField(upload_to='icecream_imgs', default="" )
    user_quantity = models.PositiveIntegerField(default=1)  # User-selected quantity
    category= models.ForeignKey(Category, default=1, on_delete=models.CASCADE)

    # Total available quantity (only visible to superusers)
    total_quantity = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.volume}"

    def is_available(self):
        return self.total_quantity > 0

class Cart(models.Model):
    icecream = models.ForeignKey(IceCream, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.FloatField()

    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
    
class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    total = models.FloatField()
    is_delivered = models.BooleanField(default=False)
    icecream = models.ForeignKey(IceCream, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + "'s " + str(self.order.date) + " " + self.icecream.name
    