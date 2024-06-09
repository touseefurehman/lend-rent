from django.db import models
from accounts.models import MyUser
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.utils import timezone

# --------------------------POST SAVE SIGNALS------------------------------#
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save

# imprting channels layers to getting current channels layer
from channels.layers import get_channel_layer
# importing asysn to sync to convert channels group methods async to sync
from asgiref.sync import async_to_sync









class Chat(models.Model):
    thread_name = models.CharField(max_length=80)
    sender = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='reciever')
    message = models.TextField()
    message_image = models.ImageField(
        upload_to='messages', null=True, blank=True)
    file = models.TextField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message












# Signals

# @receiver(post_save,sender=Chat)
# def messageNotification(sender, instance,created, **kwargs):
#     if created:
#         print('------- post save signal with like obj in if---------------')
#         # print('instance is here ', instance.sender.first_name ,nstance.user.image, instance.recipient.username , instance.time)
#         sender_name = instance.sender.name
#         print('sender name : ' , sender_name)
#         print(instance)
#         sender_id = instance.sender.id

#         sender_image = 'None'
#         receiver_id = instance.reciever.id
#         channel_layer = get_channel_layer()
#         print(channel_layer, 'channel_layer is here')
#         async_to_sync(channel_layer.group_send)(
#             'notification',
#             {
#                 'type': 'send_notification',
#                 'message': 'New Message ',
#                 'sender': sender_name,
#                  'sender_id':  sender_id,
#                 'sender_image': sender_image,
#                 'receiver_id' : receiver_id,
#             }
#             )


#     else :
#         print('------- post save signal with like obj in else---------------')
