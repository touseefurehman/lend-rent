
# import os

# from channels.routing import ProtocolTypeRouter ,  URLRouter
 
# from django.core.asgi import get_asgi_application

# import inbox.routing

# from channels.auth import AuthMiddlewareStack

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# application =ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket':AuthMiddlewareStack(URLRouter(
#         inbox.routing.urlpatterns
#     ))
    
# })
