from inbox.consumers import MyConsumer  ,NotifyConsumer
from django.urls import path 
# from django.core.asgi import get_asgi_application


urlpatterns=[
    path('ws/chat/notifications' , NotifyConsumer.as_asgi()),
    path('ws/chat/<str:group_id>', MyConsumer.as_asgi()),   
    
] 




