from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    phone_number = models.CharField(max_length=15)
    address = models.TextField() 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_reset_code = models.CharField(max_length=6, default="")