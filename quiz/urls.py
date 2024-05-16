from django.urls import path
from . import views

urlpatterns = [
    path('course-page-lecturer/<str:code>/quiz/', views.lecturer_quiz, name='lecturer-quiz'),
    path('course-page-lecturer/<str:code>/quiz/add/', views.add_quiz, name='add-quiz'),
    path('course-page-lecturer/<str:code>/quiz/<int:pk>/add-question/', views.add_question, name='add-question'),
    path('course-page-lecturer/<str:code>/quiz/<int:quiz_id>/summary/', views.quiz_summary, name='quiz-summary'),

    path('course/<str:code>/my-quizzes/', views.student_quiz, name='student-quiz'),
    path('course/<str:code>/start-quiz/<int:quiz_id>/', views.start_quiz, name='start-quiz'),
    path('course/<str:code>/student-answer/<int:quiz_id>/', views.student_answer, name='student-answer'),
    path('course/<str:code>/my-quizzes/<int:quiz_id>/quiz-result/', views.quiz_result, name='quiz-result'),
]