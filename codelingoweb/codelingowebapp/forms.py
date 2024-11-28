from django import forms
from .models import CustomUser, Question

class ProfessorSignUpForm(forms.ModelForm):
    Senha = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('Nome', 'Email', 'Senha')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.set_password(self.cleaned_data['Senha'])
        if commit:
            user.save()
        return user

class AlunoSignUpForm(forms.ModelForm):
    Senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    Matricula = forms.CharField(label='Matricula', max_length=20)

    class Meta:
        model = CustomUser
        fields = ('Nome', 'Email', 'Senha', 'Matricula')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.set_password(self.cleaned_data['Senha'])
        if commit:
            user.save()
        return user

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'difficulty']