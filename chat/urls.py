from django.contrib import admin
from django.urls import path
from chat.views import *

urlpatterns = [
    path('', Welcom.as_view(),name="welcom"),
    path('registration',Registration.as_view(), name="registration"),
    path('home',HomePage.as_view(), name="home"),
    path('deconnexion',deconnexion,name="deconnexion")
]