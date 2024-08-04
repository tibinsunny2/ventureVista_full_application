from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    phone = models.CharField(max_length=15, blank=True)
    place = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return self.username

User = get_user_model()

class Package(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    about = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField()
    location = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    # no_of_people = models.CharField(max_length=50)
    hotel = models.ImageField(upload_to='package_photos/', blank=True, null=True)
    destination = models.ImageField(upload_to='package_photos/', blank=True, null=True)
    activity = models.ImageField(upload_to='package_photos/', blank=True, null=True)
    attraction = models.ImageField(upload_to='package_photos/', blank=True, null=True)
    
    #hotel_details

    hotel_title=models.CharField(max_length=100,null=True)
    hotel_rating=models.CharField(max_length=3,null=True)
    hotel_desc = models.TextField(null=True)
    hotel_place = models.CharField(max_length=100,null=True)
    
    #Food details
    
    veg = models.TextField(null=True)
    imgveg = models.FileField(upload_to='veg food image',null=True)
    non_veg = models.TextField(null=True)
    imgnon_veg = models.FileField(upload_to='Non veg food image',null=True)
    desc_food = models.TextField(null=True)

    def __str__(self):
        return self.title

class PackageSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)
    no_of_people = models.IntegerField(null=True)
    amount=models.IntegerField(null=True)

class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(PackageSelection,on_delete=models.CASCADE,related_name="user_package")
    card_number =  models.PositiveBigIntegerField()
    cardholder = models.CharField(max_length=100)
    cvv=models.CharField(max_length=3)
    exp = models.CharField(max_length=100)
    
    

class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Blogs(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.IntegerField()
    food = models.ImageField(upload_to='blog_photos/', blank=True, null=True)
    hotel = models.ImageField(upload_to='blog_photos/', blank=True, null=True)
    travelling = models.ImageField(upload_to='blog_photos/', blank=True, null=True)
    activity = models.ImageField(upload_to='blog_photos/', blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
   
    name = models.CharField(max_length=255,blank=True,null=True)
    email=models.CharField(max_length=255,blank=True,null=True)
    review = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.review