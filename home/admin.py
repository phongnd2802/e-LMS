from django.contrib import admin
from .models import User, Student, Department, Course, Submission, Announcement, Assignment, Lecturer
from .forms import StudentAddForm, LecturerAddForm


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = [
        "get_full_name",
        "username",
        "gender",
        "email",
        "is_active",
        "is_student",
        "is_lecturer",
        "department",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_lecturer",
    ]

class StudentAdmin(admin.ModelAdmin):
    form = StudentAddForm

class LecturerAdmin(admin.ModelAdmin):
    list_display = [
        "lecturer",
        "is_approved",
    ]
    form = LecturerAddForm

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "post_date",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Submission)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Assignment)
admin.site.register(Lecturer, LecturerAdmin)