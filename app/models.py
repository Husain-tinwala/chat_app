from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatModel(models.Model):
    sender= models.CharField(max_length=100,default=None)
    message= models.TextField(null=True,blank=True)
    thread_name= models.CharField(null=True,blank=True,max_length=50)
    timestamp= models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.message

class UserProfile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True,null=True)
    online_status = models.BooleanField(default=False)

    def __str__(self)->str:
        return self.user.username