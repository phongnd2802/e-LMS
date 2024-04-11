from django.db import models
from home.models import Student, User, Course

# Create your models here.
class StudentDiscussion(models.Model):
    content = models.TextField(max_length=2000, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    send_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-sent_at',)
    
    def __str__(self):
        return self.content[:35]
    
    @property
    def time(self):
        return self.sent_at.strftime("%d-%m-%Y, %H:%M:%S")


class LecturerDiscussion(models.Model):
    content = models.TextField(max_length=2000, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    send_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-sent_at',)
    
    def __str__(self):
        return self.content[:35]
    
    @property
    def time(self):
        return self.sent_at.strftime("%d-%m-%Y, %H:%M:%S")