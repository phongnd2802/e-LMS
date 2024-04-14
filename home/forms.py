from django import forms
from .models import User, Student, GENDERS, Department, Course, Lecturer, Material, MaterialDetail
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from froala_editor.widgets import FroalaEditor
from django.forms import inlineformset_factory

class LecturerRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Họ và tên",
            }
        )
    )
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

    degree = forms.ImageField(
       required=True,
    )

    picture = forms.ImageField(
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = str(self.cleaned_data.get('full_name'))
        first_name = full_name.split()[-1]
        last_name = ' '.join(full_name.split()[:-1])
        print(first_name, last_name)
        user.first_name = first_name
        user.last_name = last_name
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.picture = self.cleaned_data.get('picture')

        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
            Lecturer.objects.create(
                lecturer=user,
                degree=self.cleaned_data.get('degree'),
                is_approved=False,
            )

        return user

    


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

class StudentAddForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=User.objects.filter(is_student=False, is_lecturer=False))

    class Meta:
        model = Student
        fields = '__all__'


class LecturerAddForm(forms.ModelForm):
    lecturer = forms.ModelChoiceField(queryset=User.objects.filter(is_student=False, is_lecturer=False))
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Lecturer
        fields = '__all__'


    def save(self, commit=True):
        lecturer_instance = super().save(commit=False)

        if lecturer_instance.is_approved:
            # Nếu is_approved của giáo viên được đặt thành True
            user_instance = lecturer_instance.lecturer
            user_instance.is_lecturer = True
            
            if self.cleaned_data.get('department'):
                # Nếu department của giáo viên được đặt
                user_instance.department = self.cleaned_data.get('department')

            user_instance.save()

        if commit:
            lecturer_instance.save()
        
        return lecturer_instance
        

class MaterialAddForm(forms.ModelForm):
    title = forms.CharField(
        max_length=1000,
        widget=forms.TextInput(attrs={
            "type": "text",
            "class": "form-control",
            "placeholder": "Tiêu đề"
        }
        )
    )
    description = forms.CharField(
        widget=FroalaEditor,
        required=False,
    )
    class Meta:
        model = Material
        fields = ('title', 'description')


class MaterialDetailAddForm(forms.ModelForm):
    name = forms.CharField(
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Tên tài liệu & video",
            }
        )
    )
    description = forms.CharField(
        widget=FroalaEditor,
        required=False
    )

    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "Link tài liệu, video",
            }
        ),
        required=False,
    )
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ),
        required=False
    )

    class Meta:
        model = MaterialDetail
        fields = [
            "name",
            "description",
            "url",
            "file",
        ]