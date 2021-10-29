from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf.urls import url

from cake.forms import UserLoginForm
from cake import views


urlpatterns = [
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('login/', views.LoginUserView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('advanced/', views.advanced_info, name='advanced_info'),
    path('confirm/', views.confirm, name='confirm'),
    path('account/', views.account, name='account'),
]


