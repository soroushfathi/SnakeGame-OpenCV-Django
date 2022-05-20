from django.urls import path
from . import views

app_name = 'App_Login'

urlpatterns = [
    path('',views.home, name='home'),
    path('sign_up/',views.sign_up, name='sign_up'),
    path('login/',views.login_page, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.change_desc_pic, name='change_profile'),
    path('add_profile/', views.add_desc_pic, name='add_profile'),
    path('edit_info/', views.edit_information, name='edit_info'),
    path('change_pass/', views.change_pass, name='change_pass'),
]
