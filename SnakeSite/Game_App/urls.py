from django.urls import path
from . import views

app_name = 'Game_App'

urlpatterns = [
    path('game/', views.game_event, name='game_event'),
    path('game_page/', views.game_page, name='game_page'),
    path('playing/', views.play, name='play'),
]
