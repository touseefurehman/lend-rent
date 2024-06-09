from django.contrib import admin

# Register your models here.
from .models import RentalItem,ItemCategory,CheckoutInfo

admin.site.register(RentalItem)
admin.site.register(ItemCategory)
admin.site.register(CheckoutInfo)

