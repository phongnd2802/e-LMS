from django.shortcuts import render, redirect
from home.decorators import lecturer_required
from django.contrib.auth.decorators import login_required
from home.models import Course, Student
from .models import Quiz, Question
from datetime import datetime, timezone
# Create your views here.

@login_required
@lecturer_required
def lecturer_quiz(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course).order_by('updated_at')
    for quiz in quizzes:
        if quiz.start < datetime.now():
            quiz.started = True
        else:
            quiz.started = False
        quiz.save()
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
                    publish_status=True if publish_status == 'on' else False, course=course)
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
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(pk=pk)
    if request.method == 'POST':
        question = str(request.POST.get('question'))
        question_image = request.POST.get('question_image')
        option1 = str(request.POST.get('option1'))
        option2 = str(request.POST.get('option2'))
        option3 = str(request.POST.get('option3'))
        option4 = str(request.POST.get('option4'))
        answer = str(request.POST.get('answer'))
        marks = float(request.POST.get('marks'))
        explanantion = str(request.POST.get('explanation'))
        explanantion_image = request.POST.get('explanantion_image')
        print(request.POST)
        print(request.FILES)
        question = Question(
            quiz=quiz,
            question=question,
            image=question_image,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            answer=answer,
            marks=marks,
            explanation_text=explanantion,
            explanation_image=explanantion_image,
        )
        question.save()
        if 'saveOnly' in request.POST:
            return redirect('lecturer-quiz', code=code)
        return render(request, 'quiz/add-question.html', {"course": course, "quiz": quiz})

    context = {
        "course": course,
        "quiz": quiz,
    }
    return render(
        request,
        'quiz/add-question.html',
        context,
    )

@login_required
def student_quiz(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course)
    student = Student.objects.get(student=request.user)

    active_quizzes = []
    previous_quizzes = []
    for quiz in quizzes:
        if quiz.end < datetime.now() or quiz.studentanswer_set.filter(student=student).exists():
            previous_quizzes.append(quiz)
        else:
            active_quizzes.append(quiz)
    
    for quiz in quizzes:
        quiz.attempted = quiz.studentanswer_set.filter(student=student).exists()
    
    for quiz in previous_quizzes:
        student_answers = quiz.studentanswer_set.filter(student=student)
        total_marks_obtained = sum([student_answer.question.marks if student_answer.answer ==
                                       student_answer.question.answer else 0 for student_answer in student_answers])
        quiz.total_marks_obtained = total_marks_obtained
        quiz.total_marks = sum(
                [question.marks for question in quiz.question_set.all()])
        quiz.percentage = round(
            total_marks_obtained / quiz.total_marks * 100, 2) if quiz.total_marks != 0 else 0
        quiz.total_questions = quiz.question_set.count()
    
    for quiz in active_quizzes:
        quiz.total_questions = quiz.question_set.count()
    
    context = {
       'course': course,
        'quizzes': quizzes,
        'active_quizzes': active_quizzes,
        'previous_quizzes': previous_quizzes,
        'student': student, 
    }
    return render(request, 'quiz/student-quiz.html', context)

@login_required
def start_quiz(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    total_questions = questions.count()

    marks = 0
    for question in questions:
        marks += question.marks
    
    quiz.total_marks = marks

    context = {
        'course': course,
        'quiz': quiz,
        'questions': questions,
        'total_questions': total_questions,
        'student': Student.objects.get(student=request.user)
    }
    return render(request, 'quiz/portal-std-new.html', context)

