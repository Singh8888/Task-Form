from django.urls import path 
from . import views
from .views import *


urlpatterns = [
   path('api/register/',  RegisterUserAPIView.as_view(), name='register'),
   path('api/login/',  LoginUserAPIView.as_view(), name='login'),
   path('',views.registration,name='registration'),
   path('login/',views.login,name='loginForm'),
]