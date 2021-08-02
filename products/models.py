from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=CASCADE)
  first_name = models.CharField(max_length=144,blank=True)
  last_name = models.CharField(max_length=144,blank=True)
  email = models.EmailField()
  signup_confirmation = models.BooleanField(default=False)
  bio = models.TextField(null=True)
  profile_picture = ImageField(upload_to='profiles')
  location = models.CharField(max_length=144,blank=True,null=True)

  def __str__(self):
      return self.user.username
  
class Product(models.Model):
  name = models.CharField(max_length=144)
  seller = models.ForeignKey(User, on_delete=CASCADE)
  description = models.TextField()
  price = models.IntegerField()
  quantity = models.IntegerField()


