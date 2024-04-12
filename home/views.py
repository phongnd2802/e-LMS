from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .models import User, Course
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, ChangePasswordForm
from admin_soft.views import logout_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
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
                if user.is_superuser:
                    return redirect('index')
                else:
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


def register(request):
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