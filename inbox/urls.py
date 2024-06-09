from django.urls import path 
from inbox.views import messages , chat_to_user
urlpatterns=[
   
    path('messages', messages , name='messages'),
    path('chat_to_user/<int:id>', chat_to_user ,name='chat_to_user'),
]
