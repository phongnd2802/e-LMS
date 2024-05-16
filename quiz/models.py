from django.db import models
from home.models import Student, Course
# Create your models here.

ANSWER = (
    ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
)


class Quiz(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_status = models.BooleanField(default=False, null=True, blank=True)
    started = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    
    def duration(self):
        return self.end - self.start
        
    def duration_in_seconds(self):
        return (self.end - self.start).total_seconds()

    def total_questions(self):
        return Question.objects.filter(quiz=self).count()

    def question_sl(self):
        return Question.objects.filter(quiz=self).count() + 1

    def total_marks(self):
        return Question.objects.filter(quiz=self).aggregate(total_marks=models.Sum('marks'))['total_marks']

    def starts(self):
        return self.start.strftime("%a, %d-%b-%y at %I:%M %p")

    def ends(self):
        return self.end.strftime("%a, %d-%b-%y at %I:%M %p")

    def attempted_students(self):
        return Student.objects.filter(studentanswer__quiz=self).distinct().count()
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField(max_length=2000)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    option1 = models.TextField(max_length=1000)
    option2 = models.TextField(max_length=1000)
    option3 = models.TextField(max_length=1000)
    option4 = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='question/', null=True)
    answer = models.CharField(max_length=1, choices=ANSWER, null=False, blank=False)

    explanation_text = models.TextField(null=True, blank=True)
    explanation_image = models.ImageField(upload_to='explanation/', null=True, blank=True)

    def __str__(self):
        return self.question
    
    @property
    def get_answer(self):
        case = {
            'A': self.option1,
            'B': self.option2,
            'C': self.option3,
            'D': self.option4,
        }
        return case[self.answer]

    def total_correct_answers(self):
        return StudentAnswer.objects.filter(question=self, answer=self.answer).count()

    def total_wrong_answers(self):
        return StudentAnswer.objects.filter(question=self).exclude(answer=self.answer).count()

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=ANSWER, default='', null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'quiz', 'question')

    def __str__(self):
        return self.student.get_full_name + ' ' + self.quiz.title + ' ' + self.question.question
    