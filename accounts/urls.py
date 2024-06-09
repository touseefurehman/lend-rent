from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login_user', views.loginuser, name='login_user'),
    path('register', views.signup, name='signup'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('forgotPassword', views.ForgetPassword, name='forgotPassword'),
    path('resetPassword/<token>', views.ChangePassword, name='resest_password'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('setup_profile/', views.setup_profile, name='setup_profile'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

