from django.contrib.auth.models import User
from django.db import models

class Wardrobe(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    image= models.ImageField(upload_to='wardrobe/')
    category= models.CharField(max_length=100)
    color= models.CharField(max_length=50)
    formality= models.CharField(max_length=100)

    def __str__(self):
        return f'{self.category} ({self.color}) - {self.user.username}'

class Occasion(models.Model):
    name= models.CharField(max_length=100)
    description= models.TextField()

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    wardrobe= models.ManyToManyField(Wardrobe)
            
    def __str__(self):
        return self.user.username
    