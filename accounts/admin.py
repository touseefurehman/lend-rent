from django.contrib import admin
from accounts.models import MyUser

admin.site.register(MyUser)



from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    model = MyUser
    
    list_display = ['username', 'mobile_number']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile_number')}),
    ) #this will allow to change these fields in admin module