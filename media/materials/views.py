from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from .models import User, Course, Lecturer, Assignment, Material, Announcement, Student, MaterialDetail, Department, Submission
from .forms import (
    RegisterForm, LoginForm,
    ProfileUpdateForm, ChangePasswordForm,
    LecturerRegisterForm, MaterialAddForm, MaterialDetailAddForm,
    AssignmentAddForm, AnnouncementForm
)
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .decorators import lecturer_required
from django.template.defaulttags import register
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
def home(request):
    students_count = User.objects.filter(is_student=True).count()
    lecturers_count = User.objects.filter(is_lecturer=True).count()
    courses_count = Course.objects.all().count()

    courses = Course.objects.filter(is_publish=True)
    student_count = courses.annotate(student_count=Count('student'))

    student_each_course = {}
    for course in student_count:
        student_each_course[course.code] = course.student_count
    
    @register.filter
    def get_item(dictionary, course_code):
        return dictionary.get(course_code)
    context = {
        "students_count": students_count,
        "lecturers_count": lecturers_count,
        "courses_count": courses_count,
        "courses": courses,
        "student_count": student_each_course
    }
    return render(
        request,
        'home/home.html',
        context
    )


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = auth.authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, f'Tên đăng nhập hoặc mật khẩu không đúng')
                return redirect('login')
    else:
        form = LoginForm()
    context = {
        "form": form,
    }

    return render(
        request,
        'home/login.html',
        context
    )


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Đăng kí thành công!'
            )
            return redirect('login')
        else:
            messages.error(
                request,
                f'Tên đăng nhập hoặc Email đã tồn tại!'
            )
            return redirect('sign-up')
    else:
        form = RegisterForm()
    
    context = {
        'form': form,
    }
    return render(
        request,
        'home/register.html',
        context
    )

def sign_up_lecturer(request):
    if request.method == 'POST':
        form = LecturerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Đã đăng kí thông tin, hãy chờ quản trị viên xem xét đăng kí của bạn!'
            )
            return redirect('login')
        else:
            messages.error(
                request,
                f'Đã có lỗi xảy ra!'
            )
            return redirect('sign-up-lecturer')
    else:
        form = LecturerRegisterForm()
    context = {
        "title": "Đăng kí giảng viên",
        "form": form,
    }
    return render(
        request,
        'home/sign-up-lecturer.html',
        context
    )


def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('home')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        user = User.objects.get(pk=int(request.user.id))
        if form.is_valid():
            try:
                form.instance.department = Department.objects.get(pk=user.department.id)
            except AttributeError as e:
                pass
            form.save()
            messages.success(request, 'Hồ sơ của bạn đã được cập nhật thành công!')
            return redirect('profile-update')
        else:
            messages.error(request, 'Hãy điền đúng các thông tin!')
    else:
        form = ProfileUpdateForm(instance=request.user)
    context = {
        "title": "Hồ sơ",
        "form": form,
    }
    return render(
        request,
        'home/profile.html',
        context
    )

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')
        if new_password == confirm_password:
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mật khẩu đã được thay đổi!')
                return redirect('profile-update')
            else:
                messages.error(request, 'Mật khẩu không hợp lệ!')
        else:
            form = ChangePasswordForm(request.user)
            messages.error(request, 'Xác nhận mật khẩu chưa khớp!')
    else:
        form = ChangePasswordForm(request.user)
    context = {
        "title": "Đổi mật khẩu",
        "form": form,
    }
    return render(
        request,
        'home/change-password.html',
       context,
    )

@login_required
def student_courses(request):
    user = get_object_or_404(User, is_student=True, pk=request.user.id)
    student = Student.objects.get(student=user)
    courses = student.course.all()
    
    all_courses = Course.objects.all()
    student_count = all_courses.annotate(student_count=Count('student'))

    student_each_course = {}
    for course in student_count:
        if course in courses:
            student_each_course[course.code] = course.student_count
    
    @register.filter
    def get_item(dictionary, course_code):
        return dictionary.get(course_code)
    context = {
        "title": "Khóa học của tôi",
        "courses": courses,
        "student": student,
        "student_count": student_each_course
    }
    return render(
        request,
        'home/student-courses.html',
        context,
    )

@login_required
@lecturer_required
def lecturer_courses(request):
    user = get_object_or_404(User, is_lecturer=True, pk=request.user.id)
    lecturer = Lecturer.objects.get(lecturer=user)
    courses = Course.objects.filter(lecturer=lecturer)

    student_count = courses.annotate(student_count=Count('student'))

    student_each_course = {}
    for course in student_count:
        student_each_course[course.code] = course.student_count
    
    @register.filter
    def get_item(dictionary, course_code):
        return dictionary.get(course_code)
    

    context = {
        "title": "Khóa học của tôi",
        "lecturer": lecturer,
        "courses": courses,
        "student_count": student_each_course,
    }
    return render(
        request,
        'home/lecturer-courses.html',
        context
    )

@login_required
@lecturer_required
def course_page_lecturer(request, code):
    course = Course.objects.get(code=code)
    try:
        announcements = Announcement.objects.filter(course_code=course)
        assignments = Assignment.objects.filter(course_code=course).order_by('created_at')
        materials = Material.objects.filter(course_code=course).order_by('created_at')
        student_count = Student.objects.filter(course=course).count()
        materials_detail = MaterialDetail.objects.filter(material_id__in=materials.values_list('pk', flat=True)).order_by('created_at')
    except:
        announcements = None
        assignments = None
        materials = None
        materials_detail = None
        student_count = 0
    print(materials_detail)
    context =  {
        "title": course.name,
        "announcements": announcements,
        "assignments": assignments,
        "materials": materials,
        "materials_detail": materials_detail,
        "student_count": student_count,
        "course": course,
    }
    return render(
        request,
        'home/course-page-lecturer.html',
        context,
    )

@login_required
@lecturer_required
def add_course_material(request, code):
    if request.method == 'POST':
        form = MaterialAddForm(request.POST)
        form.instance.course_code = Course.objects.get(code=code)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm thành công!')
            return redirect('course-page-lecturer', code=code)
        else:
            messages.error(request, 'Đã có lỗi xảy ra!')
            return redirect('add-course-material', code=code)
    else:
        form = MaterialAddForm()
    context = {
        "title": "Thêm tài liệu & video",
        "form": form,
        "action": "Thêm"
    }
    return render(
        request,
        'home/course-material.html',
        context
    )

@login_required
@lecturer_required
def edit_course_material(request, code, pk):
    instance = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialAddForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!')
            return redirect('course-page-lecturer', code=code)
    else:
        form = MaterialAddForm(instance=instance)
    context = {
        "title": f"{instance.title}",
        "form": form,
        "action": "Edit",
    }    
    return render(
        request,
        'home/course-material.html',
        context,
    )

@login_required
@lecturer_required
def delete_course_material(request, code, pk):
    instance = Material.objects.get(pk=pk)
    instance.delete()
    messages.success(request, 'Đã xóa thành công!')
    return redirect('course-page-lecturer', code=code)


@login_required
@lecturer_required
def add_course_material_detail(request, code, material_id):
    material = Material.objects.get(pk=material_id)
    course = Course.objects.get(code=code)
    if request.method == 'POST':
        form = MaterialDetailAddForm(request.POST, request.FILES)
        form.instance.material = material
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã thêm tài liệu cho {material.title} thành công!')
            return redirect('course-page-lecturer', code=code)
        else:
            messages.error(request, 'Thông tin không hợp lệ!')
            return redirect('add-course-material-detail', code=code, material_id=material_id)
    else:
        form = MaterialDetailAddForm()
    context = {
        "title": f'{material.title} | Thêm',
        "form": form,
        "material": material,
        "course": course,
        "action": "Thêm",
    }
    return render(
        request,
        'home/add-course-material.html',
        context,
    )


@login_required
@lecturer_required
def edit_course_material_detail(request, code, material_id, detail_id):
    material = Material.objects.get(pk=material_id)
    instance = get_object_or_404(MaterialDetail, pk=detail_id)
    if request.method == 'POST':
        form = MaterialDetailAddForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã chỉnh sửa thành công!')
            return redirect('course-page-lecturer', code=code)
        else:
            messages.error(request, 'Lỗi!')
            return redirect('edit-course-material-detail', code=code, material_id=material_id, detail_id=detail_id)
    else:
        form = MaterialDetailAddForm(instance=instance)
    context = {
        "title": f'{material.title} | Edit',
        "form": form,
        "action": "Edit",
    }
    return render(
        request,
        'home/add-course-material.html',
        context,
    )

@login_required
@lecturer_required
def delete_course_material_detail(request, code, material_id, detail_id):
    instance = get_object_or_404(MaterialDetail, pk=detail_id)
    instance.delete()
    messages.success(request, 'Đã xóa thành công!')
    return redirect('course-page-lecturer', code=code)


@login_required
@lecturer_required
def add_assignment(request, code):
    course = get_object_or_404(Course, code=code)
    if request.method == 'POST':
        form = AssignmentAddForm(request.POST, request.FILES)
        form.instance.course_code = course
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã tạo bài tập thành công!')
            return redirect('course-page-lecturer', code=code)
        else:
            messages.error(request, 'Lỗi!')
            return redirect('add-assignment', code=code)
    else:
        form = AssignmentAddForm()
    context = {
        "title": "Tạo bài tập",
        "form": form,
        "action": "Thêm",
    }
    return render(
        request,
        'home/add-assignment.html',
        context,
    )

@login_required
@lecturer_required
def edit_assignment(request, code, pk):
    course = get_object_or_404(Course, code=code)
    instance = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentAddForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật thành công!')
            return redirect('course-page-lecturer', code=code)
        else:
            messages.error(request, 'Đã có lỗi!')
            return redirect('edit-assignment', code=code, pk=pk)
    else:
        form = AssignmentAddForm(instance=instance)
    context = {
        "title": "Edit",
        "form": form,
        "action": "Edit",
    }
    return render(
        request,
        'home/edit-assignment.html',
        context
    )

@login_required
@lecturer_required
def delete_assignment(request, code, pk):
    instance = get_object_or_404(Assignment, pk=pk)
    instance.delete()
    messages.success(request, 'Đã xóa thành công')
    return redirect('course-page-lecturer', code=code)


@login_required
@lecturer_required
def add_announcement(request, code):
    course = Course.objects.get(code=code)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        form.instance.course_code = course
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm thông báo thành công!')
            return redirect('course-page-lecturer', code=code)
        else:
            messages.error(request, 'Lỗi xảy ra!')
            return redirect('add-announcement', code=code)
    else:
        form = AnnouncementForm()
    context = {
        "title": "Thêm thông báo",
        "form": form,
        "action": "Thêm",
    }
    return render(
        request,
        'home/announcement.html',
        context
    )

@login_required
@lecturer_required
def edit_announcement(request, code, pk):
    instance = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã sửa thông báo thành công!')
            return redirect('course-page-lecturer', code=code)
        else:
            messages.error(request, 'Lỗi!')
            return redirect('edit-announcement', code=code, pk=pk)
    else:
        form = AnnouncementForm(instance=instance)
    context = {
        "title": "Chỉnh sửa thông báo",
        "form": form,
        "action": "Edit",
    }
    return render(
        request,
        'home/announcement.html',
        context,
    )

@login_required
@lecturer_required
def delete_annoucement(request, code, pk):
    instance = get_object_or_404(Announcement, pk=pk)
    instance.delete()
    messages.success(request, 'Đã xóa thông báo thành công!')
    return redirect('course-page-lecturer', code=code)


@login_required
@lecturer_required
def publish_course(request, code):
    if request.method == 'POST':
        course = get_object_or_404(Course, code=code)
        is_checked = request.POST.get('is_checked')
        if is_checked == "true":
            course.is_publish = True
        else:
            course.is_publish = False
        course.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def course_detail(request, code):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(student=request.user)
            courses = student.course.all()
            course = get_object_or_404(Course, code=code)
            if course in courses:
                return redirect('course-page', code=code) 
        except ObjectDoesNotExist:
            course = get_object_or_404(Course, code=code)
            if course.lecturer.lecturer == request.user:
                return redirect('course-page', code=code)
    course = get_object_or_404(Course, code=code)
    materials = Material.objects.filter(course_code=course).order_by('created_at')
    materials_detail = MaterialDetail.objects.filter(material_id__in=materials.values_list('pk', flat=True)).order_by('created_at')
    context = {
        "title": course.name,
        "course": course,
        "materials": materials,
        "materials_detail": materials_detail,
    }
    return render(
        request,
        'home/course-detail.html',
        context 
    )

@login_required
def enroll_course(request, code):
    course = Course.objects.get(code=code)
    student = Student.objects.get(student=request.user)
    if request.method == 'POST':
        key = request.POST.get('key')
        if key == str(course.student_key):
            student.course.add(course)
            student.save()
            return redirect('course-page', code=code)
        else:
            messages.error(request, 'Mã không đúng!')
            return redirect('enroll-course', code=code)
    return render(
        request,
        'home/enroll-course.html',
    )

@login_required
def course_page(request, code):
    course = Course.objects.get(code=code)
    try:
        announcements = Announcement.objects.filter(course_code=course)
        assignments = Assignment.objects.filter(course_code=course).order_by('created_at')
        materials = Material.objects.filter(course_code=course).order_by('created_at')
        student_count = Student.objects.filter(course=course).count()
        materials_detail = MaterialDetail.objects.filter(material_id__in=materials.values_list('pk', flat=True)).order_by('created_at')
    except:
        announcements = None
        assignments = None
        materials = None
        materials_detail = None
        student_count = 0
    context =  {
        "title": course.name,
        "announcements": announcements,
        "assignments": assignments,
        "materials": materials,
        "materials_detail": materials_detail,
        "student_count": student_count,
        "course": course,
    }
    return render(
        request,
        'home/course-page-lecturer.html',
        context,
    )

@login_required
def add_submission(request, code, pk):
    course = Course.objects.get(code=code)
    assignment = Assignment.objects.get(pk=pk)
    not_submit = False
    if assignment.due_date < datetime.now().strftime("%d-%m-%Y, %I:%M:%S %p"):
        not_submit = True

    if request.method == 'POST' and request.FILES:
        assignment = Assignment.objects.get(pk=pk)
        submission = Submission(assignment=assignment, student=Student.objects.get(student=request.user),
                                file=request.FILES['file'])
        submission.status = "Đã nộp!"
        submission.save()
        return redirect('add-submission', code=code, pk=pk)
    else:
        assignment = Assignment.objects.get(pk=pk)
        student = Student.objects.get(student=request.user)
        try:
            submission = Submission.objects.get(assignment=assignment, student=student)
            return redirect('edit-submission', code=code, pk=pk)
        except ObjectDoesNotExist:
            submission = None
    context = {
        'assignment': assignment,
        'course': course,
        'submission': submission,
        'student': Student.objects.get(student=request.user),
        'courses': Student.objects.get(student=request.user).course.all(),
        "not_submit": not_submit,
        "action": "Nộp bài",
    }
    return render(request, 'home/assignment-portal.html', context)

@login_required
def edit_submission(request, code, pk):
    course = Course.objects.get(code=code)
    assignment = Assignment.objects.get(pk=pk)
    submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(student=request.user))
    if assignment.due_date < datetime.now().strftime("%d-%m-%Y, %I:%M:%S %p"):
        pass

    if request.method == 'POST' and request.FILES:
        submission.file = request.FILES['file']
        submission.status = "Đã nộp lại!"
        submission.save()
        return redirect('edit-submission', code=code, pk=pk)
    else:
        assignment = Assignment.objects.get(pk=pk)
        submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(student=request.user))
    context = {
        "course": course,
        "assignment": assignment,
        "submission": submission,
        "action": "Chỉnh sửa bài nộp",
    }
    return render(request, 'home/assignment-portal.html', context)

@login_required
@lecturer_required
def view_all_submission(request, code, pk):
    course = Course.objects.get(code=code)
    assignment = Assignment.objects.get(pk=pk)
    submissions = Submission.objects.filter(assignment=assignment)
    total_students = Student.objects.filter(course=course).count()
    context = {
        "submissions": submissions,
        "course": course,
        "assignment": assignment,
        "total_students": total_students,
    }
    return render(
        request,
        'home/view-submissions.html',
        context
    )

@login_required
@lecturer_required
def grade_submission(request, code, assign_id, pk):
    if request.method == 'POST':
        course = Course.objects.get(code=code)
        assignment = Assignment.objects.get(pk=assign_id)
        submission = Submission.objects.get(pk=pk)
        marks = float(request.POST.get('marks'))
        submission.marks = marks
        submission.save()
        return redirect('view-submissions', code=code, pk=assign_id)
    else:
        return redirect('view-submissions', code=code, pk=assign_id)