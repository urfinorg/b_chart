from django.contrib import admin
from django.urls import path

from b_chat_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api', views.api, name='api')
]
