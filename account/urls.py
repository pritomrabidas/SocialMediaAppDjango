from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register, name='register'),
    path('varification/', varification, name='varification'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]