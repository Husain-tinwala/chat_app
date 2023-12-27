from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save,sender=UserProfile)
def send_online_status(sender,instance , created, **kwargs):
    if not created:
        channel_layer=get_channel_layer()
        user = instance.user.username
        user_status= instance.online_status

        data ={
            'username':user,
            'status':user_status
        }