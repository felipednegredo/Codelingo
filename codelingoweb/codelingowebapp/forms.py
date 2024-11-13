from django import forms
from .models import CustomUser

class ProfessorSignUpForm(forms.ModelForm):
    Senha = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('Nome', 'Email', 'Senha')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_professor = True
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
        user.is_aluno = True
        user.set_password(self.cleaned_data['Senha'])
        if commit:
            user.save()
        return user