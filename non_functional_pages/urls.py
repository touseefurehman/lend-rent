from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views 
from items import urls
#from log import urls
urlpatterns = [
    path('forget/', views.forget, name='forget'),
    path('reset/', views.pass_reset, name='reset'),
    path('', views.home, name='home'),
    path('rent/', views.rent, name='rent'),
    path('lend/', views.lend, name='lend'),
    path('search/', views.search, name='search'),  
    path('rental/', views.rental, name='rental'),  
    path('rental_list/', views.rental_list, name='rental_list'), 
    path('search/', views.checkout, name='search'),   
    path('confirm/', views.confirm, name='search'),   




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)