from django.contrib import admin
from cake import views
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('advanced', views.advanced_info, name='advanced_info'),
]


