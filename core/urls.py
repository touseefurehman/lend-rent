from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from items import urls
from rating import urls
from non_functional_pages import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/' , include('accounts.urls'),name='accounts'),
    path('accounts/', include('allauth.urls')),
    path('items/',include('items.urls'),name='list_an_item'),
    path('items/',include('items.urls'),name='list_an_item'),
    path('pdp/',include("rating.urls")) ,   
    path('',include('non_functional_pages.urls'),name='non_functional_pages'), 



] + static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)
