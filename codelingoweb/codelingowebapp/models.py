from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .validators import alphanumeric_password_validator
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    Nome = models.CharField(max_length=255)
    Email = models.EmailField(unique=True, validators=[EmailValidator()])
    Senha = models.CharField(max_length=255, validators=[alphanumeric_password_validator])
    Matricula = models.CharField(max_length=20, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    completedphases_set = models.ManyToManyField('CompletedPhases', related_name='customuser_set', blank=True)

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class Phase(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    #questions = models.ManyToManyField(Question, related_name='phases', blank=True)

    def __str__(self):
        return self.name

class Trail(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    #phases = models.ManyToManyField(Phase, related_name='trails', blank=True)

    def __str__(self):
        return f'{self.name} - {self.description}'

    def is_user_enrolled(self, user):
        return Enrollment.objects.filter(user=user, trail=self).exists()

class Enrollment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.trail.name}'

class TrailPhases(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, default=1)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, default=1)
    unlocked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.trail} - {self.phase}'

class PhaseQuestions(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.phase} - {self.question}'

class UserResponse(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    question_difficulty = models.CharField(max_length=255)
    response_time = models.IntegerField()


class CompletedPhases(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='completed_phases')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    time_spent = models.IntegerField()

    class Meta:
        unique_together = ('user', 'phase')