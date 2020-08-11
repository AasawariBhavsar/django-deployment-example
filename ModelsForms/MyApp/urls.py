from django.urls import path
from MyApp import views

app_name='MyApp'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login')
    
]