from django import forms
from .models import Question, ANSWER
from froala_editor.widgets import FroalaEditor

class QuestionAddForm(forms.ModelForm):
    question = forms.CharField(
        widget=FroalaEditor,
        required=True,
    )

    image = forms.ImageField(
        required=False,
    )

    option1 = forms.CharField(
        widget=FroalaEditor,
    )
    option2 = forms.CharField(
        widget=FroalaEditor,
    )
    option3 = forms.CharField(
        widget=FroalaEditor,
    )
    option4 = forms.CharField(
        widget=FroalaEditor,
    )

    answer = forms.CharField(
        widget=forms.Select(
            choices=ANSWER,
            attrs={
                "class": "browser-default custom-select form-control",
            }
        )
    )
    marks = forms.DecimalField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    explanation_text = forms.CharField(
        widget=FroalaEditor,
        required=False,
    )

    explanation_image = forms.ImageField(
        required=False
    )
    
    class Meta:
        model = Question
        fields = ('question', 'image', 'option1', 'option2', 'option3',
                  'option4', 'answer', 'marks', 'explanation_text', 'explanation_image')

