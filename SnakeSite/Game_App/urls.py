from django.urls import path
from . import views

app_name = 'Game_App'

urlpatterns = [
    path('playing/',views.play, name='play'),
]
