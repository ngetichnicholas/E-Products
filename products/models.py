from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField
from django.core.validators import MaxLengthValidator,MinLengthValidator

# Create your models here.
class User(AbstractUser):
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []#removes email from REQUIRED_FIELDS
  is_admin = models.BooleanField(default=False)
  is_customer = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  full_name = models.CharField(max_length=144,blank=True)
  email = models.EmailField(unique=True)
  signup_confirmation = models.BooleanField(default=False)
  bio = models.TextField(null=True)
  profile_picture = ImageField(upload_to='profiles')
  location = models.CharField(max_length=144,blank=True,null=True)
  phone = models.CharField(max_length=13, null=True,blank=True, validators=[MinLengthValidator(10),MaxLengthValidator(13)])

  
  def __str__(self):
      return self.username

class Category(models.Model):
  name = models.CharField(max_length=40)
  
class Product(models.Model):
  name = models.CharField(max_length=144)
  category = models.ForeignKey(Category,on_delete=CASCADE)
  description = models.TextField()
  price = models.IntegerField()
  quantity = models.IntegerField()
  image = models.ImageField(upload_to = 'products')

  def __str__(self):
      return self.name


