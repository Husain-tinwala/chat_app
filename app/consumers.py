import json
from app.serializer import ChatModelSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from app.models import ChatModel, UserProfile
from django.contrib.auth.models import User

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("In connect")
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'  # Fix the typo here
        
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()


    async def disconnect(self, code):
        print("In disconnect")
        await self.channel_layer.group_discard(  
            self.room_group_name,
            self.channel_name  
        )


    async def receive(self, text_data=None, bytes_data=None):
        print("In recieve")
        data = json.loads(text_data)
        message_data = {
            'sender': data['username'],
            'message': data['message'],
            'thread_name': self.room_group_name,
        }

        saved_message = await self.save_message(message_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'saved_message': saved_message,
            }
        )
    
    async def chat_message(self, event):
        print("In chat message")
        type = event['type'] 
        message = event['saved_message']

        await self.send(text_data=json.dumps({
            'message': message,
            'type': type
        }))
    

    @database_sync_to_async
    def save_message(self, message_data):
        print("In save message")
        saved_message = ChatModel.objects.create(**message_data)
        serializer = ChatModelSerializer(saved_message)
        return serializer.data

    

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name= 'user'

        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
    
        await self.accept()
    
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    async def receive(self, text_data=None, bytes_data=None):
        data= json.loads(text_data)
        username = data['username']
        connection_type= data['type']
        await self.change_online_status(username,connection_type)

    @database_sync_to_async
    def change_online_status(self,username,c_type):
        userprofile = UserProfile.objects.get(user__username = username)
        if c_type=='open':
            userprofile.online_status=True
        else:
            userprofile.online_status=False
        userprofile.save()