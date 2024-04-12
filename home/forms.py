from django import forms
from .models import User, Student, GENDERS, Department
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Tên đăng nhập",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "Email",
            }
        )
    )

    password1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Mật khẩu"
            }
        ),
    )

    password2 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Xác nhận mật khẩu"
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')

        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
            Student.objects.create(
                student=user,

            )

        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Tên đăng nhập",
            }
        )
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Mật khẩu",
            }
        )
    )


class ProfileUpdateForm(UserChangeForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        )
    )

    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            }
        )
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control", "disabled": "disabled"}
        ),  
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "department",
        ]


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Mật khẩu cũ"
            }
        ),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Mật khẩu mới"
            }
        ),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Xác nhận mật khẩu"
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "old_password",
            "new_password1",
            "new_passwrod2",
        ]
