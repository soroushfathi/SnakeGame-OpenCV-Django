from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('App_Login.urls')),
    path('playing/',include('Game_App.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)