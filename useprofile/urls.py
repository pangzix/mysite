from  django.urls import path
from .views import user_login,user_logout,user_register,profile_edit

app_name = 'userprofile'

urlpatterns = [
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('register/',user_register,name='register'),
    path('edit/<int:id>/',profile_edit,name='edit'),
]