from django.urls import path, include
from items import views

urlpatterns = [
path('list_an_item/',views.rental_item_form,name='list_an_item'),    
path('search_by_category/<int:id_cat>',views.test, name="search_by_category"),
path('search_by_list/',views.test, name="search_by_list"),
path('edit_item/<int:item_id>', views.edit_item, name='edit_item'),      
path('my_item/', views.my_item, name='my_item'), 
path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
path('Home/', views.Category, name='Category'),
path('checkout/<int:category_id>/<int:rental_item_id>/', views.checkout, name='checkout'),
    path("success/", views.success, name="success"),
path("cancel/", views.cancel, name="cancel"),
]
