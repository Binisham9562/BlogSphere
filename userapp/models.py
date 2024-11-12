from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class CategoryAbstract(models.Model):
    # slug = models.SlugField(max_length=100, unique=True,blank=True)
    created_user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    class Meta:
        abstract=True
   
class Category(CategoryAbstract):
    category_name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural="Category"
    def __str__(self):
        return self.category_name
     

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username}'s Profile"
