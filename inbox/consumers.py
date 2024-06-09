from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
from inbox.models import Chat
from accounts.models import MyUser
from channels.db import database_sync_to_async
import base64
from django.core.files.base import ContentFile


# Async
class MyConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        print('websocket connected chat ')
        other_user_id = self.scope['url_route']['kwargs']['group_id']
        my_id = self.scope['user'].id
        print(other_user_id, my_id)




        if int(other_user_id) > int(my_id):
            self.group_name = f'chats{other_user_id}-{my_id}'
        else:
            self.group_name = f'chats{my_id}-{other_user_id}'






        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

















    async def receive(self, text_data=None, bytes_data=None):

        print('websocket receive', text_data)
        other_user_id = self.scope['url_route']['kwargs']['group_id']
        my_id = self.scope['user'].id
        #  Chat DB
        sender = await database_sync_to_async(MyUser.objects.get)(id=my_id)
        recever = await database_sync_to_async(MyUser.objects.get)(id=other_user_id)

        # chat=Chat(thread_name=self.group_name)
        print('Info', sender, recever,  self.group_name)

        data = json.loads(text_data)
        message = data['msg']
        image = data['msg_img']
        if image:
            image = 'data:image/png;base64,'+data['msg_img']
            print(image)

        if data['msg'] and not image:

            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.message',
                'message': data

            })
            new_msg = await database_sync_to_async(Chat.objects.create)(thread_name=self.group_name, sender=sender, reciever=recever, message=message,  is_seen=False)

        else:
            # Convert Image base 64 into python image and save in database
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            # You can save this as file instance.
            img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

            print('Image : ', img)

            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.message',
                'message': data

            })
            new_msg = await database_sync_to_async(Chat.objects.create)(thread_name=self.group_name, sender=sender, reciever=recever, message=message, message_image=img, is_seen=False)

    async def chat_message(self, text_data):
        # print('Send Data  :', text_data)
        data = text_data['message']
        print(data)
        my_id = self.scope['user'].id
        print('actuall data : ')
        if data:
            await self.send(
                text_data=json.dumps(text_data['message'])
            )

    async def disconnect(self, close_code):
        print('websocket Disconnected', close_code)
        print('Channel Layer : ', self.channel_layer)
        print('Channel Name : ', self.channel_name)
        # Discard Group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


# Notification

class NotifyConsumer(WebsocketConsumer):
    def websocket_connect(self, event):
        print(self.channel_layer, 'layer')
        # self.notify_group_name = 'notifications'
        async_to_sync(self.channel_layer.group_add)(
            'notifications',
            self.channel_name
        )
        print('channels in connecting state ')
        self.accept()

    def websocket_receive(self, event):
        print('event', event)
        data = json.loads(event['text'])
        print(data)
        message = data['message']
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': message,
            }
        )

    def send_notification(self, event , type='send_notification'):
        print('now we are in send msg notify state', event)
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message,
        }))

    def websocket_disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            'notifications',
            self.channel_name
        )
        raise StopConsumer()
