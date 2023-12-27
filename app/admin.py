from django.contrib import admin
from .models import ChatModel, UserProfile
# Register your models here.
admin.site.register(ChatModel)
admin.site.register(UserProfile)