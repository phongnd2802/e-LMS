from django.db import models
from django.contrib.auth.models import AbstractUser

GENDERS = (
    ("M", "Nam"),
    ("F", "Nữ"),
)

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
        


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDERS, null=True)
    picture = models.ImageField(
        upload_to='profile_pictures/', default="profile_pictures/default.png", null=True
    )
    email = models.EmailField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('-date_joined',)

    @property
    def get_full_name(self) -> str:
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.last_name + " " + self.first_name
        return full_name
    
    def __str__(self):
        return f"{self.username} ({self.get_full_name})"
    
    @property
    def get_user_role(self):
        if self.is_superuser:
            role = "Admin"
        elif self.is_student:
            role = "Student"
        elif self.is_lecturer:
            role = "Lecturer"
        
        return role

    def delete(self, *args, **kwargs):
        if self.picture != 'profile_pictures/default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)

    

class Lecturer(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.ImageField(upload_to='degree/', blank=False, null=False)
    is_approved = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        ordering = ('-lecturer__date_joined',)
    
    def __str__(self):
        return self.lecturer.get_full_name

class Course(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255, null=False)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=False, related_name='courses'
    )
    picture = models.ImageField(upload_to='courses/', default='courses/default.jpg', null=True)
    lecturer = models.ForeignKey(
        Lecturer, on_delete=models.SET_NULL, null=True, blank=True
    )
    student_key = models.CharField(max_length=100, null=True, blank=True)
    lecturer_key = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('code', 'name', 'department')
    
    def __str__(self):
        return f'{self.name} ({self.code})'
    


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, blank=True)
    
    class Meta:
        ordering = ('-student__date_joined',)

    def __str__(self):
        return self.student.get_full_name
    



class Announcement(models.Model):
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    description = models.TextField(max_length=2000, null=False, blank=False)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.description
    
    @property
    def post_date(self):
        return self.created_at.strftime("%d-%m-%Y, %I:%M:%S %p")


class Assignment(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False
    )
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=False)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    @property
    def post_date(self):
        return self.updated_at.strftime("%d-%m-%Y, %I:%M:%S %p")
    
    @property
    def due_date(self):
        return self.deadline.strftime("%d-%m-%Y, %I:%M:%S %p")
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=False
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to='submissions/', null=True)
    submited_date = models.DateTimeField(auto_now_add=True, null=False)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.student.student.get_full_name + " - " + self.assignment.title

    @property
    def file_name(self):
        return self.file.name.split('/')[-1]
    
    @property
    def time_difference(self):
        difference = self.assignment.deadline - self.submited_date
        days = difference.days
        hours = difference.seconds // 3600
        minutes = (difference.seconds // 60) % 60
        seconds = difference.seconds % 60

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    return str(seconds) + " giây"
                else:
                    return str(minutes) + " phút " + str(seconds) + " giây"
            else:
                return str(hours) + " giờ " + str(minutes) + " phút " + str(seconds) + "giây"
        else:
            return str(days) + " ngày " + str(hours) + " giờ " + str(minutes) + " phút " + str(seconds) + " giây"
        
    @property
    def submission_date(self):
        return self.submited_date.strftime("%d-%m-%Y, %I:%M:%S %p")

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('-submited_date',)

    

class Material(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    #file = models.FileField(upload_to='materials/', null=True, blank=True)


    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    

    @property
    def post_date(self):
        return self.created_at.strftime("%d-%m-%Y, %I:%M:%S %p")


class MaterialDetail(models.Model):
    name = models.CharField(max_length=1000, null=False, blank=False)
    description = models.TextField(max_length=5000, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-created_at',)
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    @property
    def post_date(self):
        return self.updated_at.strftime("%d-%m-%Y, %I:%M:%S %p")

