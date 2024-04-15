from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from .models import User, Course, Lecturer, Assignment, Material, Announcement, Student, MaterialDetail
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

# Create your views here.
def home(request):
    students = User.objects.filter(is_student=True).count()
    lecturers = User.objects.filter(is_lecturer=True).count()
    courses = Course.objects.all().count()
    context = {
        "students": students,
        "lecturers": lecturers,
        "courses": courses,
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
            return redirect('sign-up')
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
            return redirect('sign-up-lecturer')
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
        if form.is_valid():
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
    
    context = {}
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
        pass
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
        'home/assignment.html',
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
        'home/assignment.html',
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

