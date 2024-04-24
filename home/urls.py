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
    path('student-courses/', views.student_courses, name='student-courses'),

    #CRUD course content
    path('course-page-lecturer/<str:code>/', views.course_page_lecturer, name='course-page-lecturer'),
    path('course-page-lecturer/<str:code>/add-material/', views.add_course_material, name='add-course-material'),
    path('course-page-leturer/<str:code>/<int:pk>/edit/', views.edit_course_material, name='edit-course-material'),
    path('course-page-lecturer/<str:code>/<int:pk>/delete/', views.delete_course_material, name='delete-course-material'),
    path('course-page-lecturer/<str:code>/<int:material_id>/add/', views.add_course_material_detail, name='add-course-material-detail'),
    path('course-page-lecturer/<str:code>/<int:material_id>/<int:detail_id>/edit/', views.edit_course_material_detail, name='edit-course-material-detail'),
    path('course-page-lecturer/<str:code>/<int:material_id>/<int:detail_id>/delete/', views.delete_course_material_detail, name='delete-course-material-detail'),

    #CRUD Assignment
    path('course-page-lecturer/<str:code>/assignment/add/', views.add_assignment, name='add-assignment'),
    path('course-page-lecturer/<str:code>/assignment/<int:pk>/edit/', views.edit_assignment, name='edit-assignment'),
    path('course-page-lecturer/<str:code>/assignment/<int:pk>/delete/', views.delete_assignment, name='delete-assignment'),

    #CRUD Announcement
    path('course-page-lecturer/<str:code>/announcement/add/', views.add_announcement, name='add-announcement'),
    path('course-page-lecturer/<str:code>/announcement/<int:pk>/edit/', views.edit_announcement, name='edit-announcement'),
    path('course-page-lecturer/<str:code>/announcement/<int:pk>/delete/', views.delete_annoucement, name='delete-announcement'),


    path('course/<str:code>/detail/', views.course_detail, name='course-detail'),
    path('course/<str:code>/detail/enroll/', views.enroll_course, name='enroll-course'),
    path('course-page/<str:code>/', views.course_page, name='course-page'),

    path('course/<str:code>/assignment/<int:pk>/add-submission/', views.add_submission, name='add-submission'),
    path('course/<str:code>/assignment/<int:pk>/edit-submission/', views.edit_submission, name='edit-submission'),
    path('course-page-lecturer/<str:code>/assignment/<int:pk>/view-submissions/', views.view_all_submission, name='view-submissions'),
    path('course-page-lecturer/<str:code>/assignment/<int:assign_id>/grade-submission/<int:pk>/', views.grade_submission, name='grade-submission'),
]