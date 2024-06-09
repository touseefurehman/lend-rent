from django.urls import path

from rating import views


urlpatterns = [

path('pdp/<int:id_cat>/<int:rental_item_id>', views.pdp, name='pdp'),

     

]


