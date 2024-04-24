from django.urls import path
from . import views

urlpatterns = [
    path('course-page-lecturer/<str:code>/quiz/', views.lecturer_quiz, name='lecturer-quiz'),
    path('course-page-lecturer/<str:code>/quiz/add/', views.add_quiz, name='add-quiz'),
    path('course-page-lecturer/<str:code>/quiz/<int:pk/add-question/', views.add_question, name='add-question'),
]