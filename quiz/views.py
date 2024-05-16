from django.shortcuts import render, redirect
from home.decorators import lecturer_required
from django.contrib.auth.decorators import login_required
from home.models import Course, Student, Lecturer
from .models import Quiz, Question, StudentAnswer
from .forms import QuestionAddForm
from datetime import datetime
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
        print(publish_status)
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
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.quiz = quiz
            form.save()
            if 'saveOnly' in request.POST:
                return redirect('lecturer-quiz', code=code)
            return render(request, 'quiz/add-question.html', {"course": course, "quiz": quiz})
        else:
            return redirect('course-page-lecturer', code=code)
    else:
        form = QuestionAddForm()
    context = {
        "course": course,
        "quiz": quiz,
        "form": form,
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

@login_required
def student_answer(request, code, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    student = Student.objects.get(student=request.user)

    for question in questions:
        answer = request.POST.get(str(question.id))
        student_ans = StudentAnswer(student=student, quiz=quiz, question=question, 
                                    answer=answer, marks=question.marks if answer == question.answer else 0)
        try:
            student_ans.save()
        except:
            return redirect('student-quiz', code=code)
    return redirect('student-quiz', code=code)


@login_required
@lecturer_required
def quiz_summary(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    time = datetime.now()
    total_students = Student.objects.filter(course=course).count()
    for question in questions:
        question.A = StudentAnswer.objects.filter(
            question=question, answer='A').count()
        question.B = StudentAnswer.objects.filter(
            question=question, answer='B'
        ).count()
        question.C = StudentAnswer.objects.filter(
            question=question, answer='C'
        ).count()
        question.D = StudentAnswer.objects.filter(
            question=question, answer='D'
        ).count()
    
    students = Student.objects.filter(course=course)
    for student in students:
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=quiz
        )
        total_marks_obtained = 0
        for student_ans in student_answers:
            total_marks_obtained += student_ans.question.marks if student_ans.answer == student_ans.question.answer else 0
        student.total_marks_obtained = total_marks_obtained

    if request.method == 'POST':
        quiz.publish_status = True
        quiz.save()
        return redirect('quiz-summary', code=code, quiz_id=quiz_id)
    
    for student in students:
        if StudentAnswer.objects.filter(student=student, quiz=quiz).count() > 0:
            student.attempted = True
        else:
            student.attempted = False
    
    for student in students:
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=quiz)
        for student_answer in student_answers:
            student.submission_time = student_answer.created_at.strftime(
                "%a, %d-%b-%y at %I:%M %p")
            
    context = {
        'course': course, 
        'quiz': quiz, 
        'questions': questions, 
        'time': time, 
        'total_students': total_students,
        'students': students, 
        'lecturer': Lecturer.objects.get(lecturer=request.user)
    }
    return render(request, 'quiz/quiz-summary.html', context)

@login_required
def quiz_result(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    try:
        student = Student.objects.get(student=request.user)
        student_answers = StudentAnswer.objects.filter(student=student, quiz=quiz)
        total_marks_obtained = 0
        for student_ans in student_answers:
            total_marks_obtained += student_ans.question.marks if student_ans.answer == student_ans.question.answer else 0
        quiz.total_marks_obtained = total_marks_obtained
        quiz.total_marks = 0
        for question in questions:
            quiz.total_marks += question.marks
        quiz.percentage = (total_marks_obtained / quiz.total_marks) * 100
        quiz.percentage = round(quiz.percentage, 2)
    except:
        quiz.total_marks_obtained = 0
        quiz.total_marks = 0
        quiz.percentage = 0
    
    for question in questions:
        student_ans = StudentAnswer.objects.get(
            student=student, question=question
        )
        question.student_answer = student_ans.answer
    
    student_answers = StudentAnswer.objects.filter(
        student=student, quiz=quiz
    )
    for student_ans in student_answers:
        quiz.time_taken = student_ans.created_at - quiz.start
        quiz.time_taken = quiz.time_taken.total_seconds()
        quiz.time_taken = round(quiz.time_taken, 2)
        quiz.submission_time = student_ans.created_at.strftime(
                "%a, %d-%b-%y at %I:%M %p")
        
    context = {
        'course': course,
        'quiz': quiz,
        'questions': questions,
        'student': student
    }
    return render(request, 'quiz/quiz-result.html', context)