from django.urls import path
from . import views
from admin_soft import views as admin_views

urlpatterns = [
    path('admin/', admin_views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('sign-up/', views.register_user, name='sign-up'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_update, name='profile-update'),
    path('change-password/', views.change_password, name='change-password'),
    path('sign-up-lecturer/', views.sign_up_lecturer, name='sign-up-lecturer'),
    path('lecturer-courses/', views.lecturer_courses, name='lecturer-courses'),
    path('course-page-lecturer/<str:code>/', views.course_page_lecturer, name='course-page-lecturer'),
    path('course-page-lecturer/<str:code>/add-material/', views.add_course_material, name='add-course-material'),
]