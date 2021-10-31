from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.urls import path

from cake.forms import UserLoginForm
from cake import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('login/', views.LoginUserView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('advanced/', views.advanced_info, name='advanced_info'),
    path('confirm/', views.confirm, name='confirm'),
    path('account/', views.account, name='account'),
    path('cancel_order/<int:order_id>', views.cancel_order, name='cancel_order')
] + static(settings.DOCS_URL, document_root=settings.DOCS_DIR)


