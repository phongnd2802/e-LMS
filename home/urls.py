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
    path('course-page-leturer/<str:code>/<int:pk>/edit/', views.edit_course_material, name='edit-course-material'),
    path('course-page-lecturer/<str:code>/<int:pk>/delete/', views.delete_course_material, name='delete-course-material'),
    path('course-page-lecturer/<str:code>/<int:material_id>/add/', views.add_course_material_detail, name='add-course-material-detail'),
    path('course-page-lecturer/<str:code>/<int:material_id>/<int:detail_id>/edit/', views.edit_course_material_detail, name='edit-course-material-detail'),
    path('course-page-lecturer/<str:code>/<int:material_id>/<int:detail_id>/delete/', views.delete_course_material_detail, name='delete-course-material-detail'),
]