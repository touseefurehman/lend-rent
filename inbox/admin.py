from django.contrib import admin
from inbox.models import  Chat
# Register your models here.


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread_name', 'sender',
                    'reciever', 'message', 'file', 'is_seen', 'timestamp']
