from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=144)
  seller = models.ForeignKey(User, on_delete=CASCADE)
  description = models.TextField()
  price = models.IntegerField()
  quantity = models.IntegerField()


