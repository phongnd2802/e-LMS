from django.shortcuts import render, redirect
from home.decorators import lecturer_required
from django.contrib.auth.decorators import login_required
from home.models import Course
from .models import Quiz
# Create your views here.

@login_required
@lecturer_required
def lecturer_quiz(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course).order_by('updated_at')
    context = {
        "course": course,
        "quizzes": quizzes,
    }
    return render(
        request,
        'quiz/quiz.html',
        context,
    )

@login_required
@lecturer_required
def add_quiz(request, code):
    course = Course.objects.get(code=code)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start = request.POST.get('start')
        end = request.POST.get('end')
        publish_status = request.POST.get('checkbox')
        quiz = Quiz(title=title, description=description, start=start, end=end,
                    publish_status=publish_status, course=course)
        quiz.save()
        return redirect('lecturer-quiz', code=code)
    context = {
        "course": course,
    }
    return render(
        request,
        'quiz/add-quiz.html',
        context,
    )

@login_required
@lecturer_required
def add_question(request, code, pk):
    return render(
        request,
        'quiz/add-question.html'
    )
