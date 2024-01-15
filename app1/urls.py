from django.contrib import admin
from django.urls import path
from . import views 

app_name = 'app1'

urlpatterns = [
    path('', views.registration, name='registration'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('wall', views.wall, name='wall'),
    path('message', views.message, name='message'),
    path('comment', views.comment, name='comment')
]

