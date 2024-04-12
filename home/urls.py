from django.urls import path
from . import views
from admin_soft import views as admin_views

urlpatterns = [
    path('admin/', admin_views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('sign-up/', views.register, name='sign-up'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_update, name='profile-update'),
    path('change-password/', views.change_password, name='change-password'),
]