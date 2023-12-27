from django.shortcuts import render
from django.contrib.auth.models import User

from app.models import ChatModel
# Create your views here.


def index(request):
    users= User.objects.exclude(username= request.user.username)
    return render(request, 'index.html', context={'users':users})

def chat_page(request,username):
    user_obj = User.objects.get(username=username)
    users= User.objects.exclude(username = request.user.username)

    if request.user.id> user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    
    messages_obj= ChatModel.objects.filter(thread_name=thread_name)

    return render(request, 'main_chat.html', context={'users':users,'user':user_obj,"messages":messages_obj})
