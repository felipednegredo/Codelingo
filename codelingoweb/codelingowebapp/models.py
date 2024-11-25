from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    is_professor = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)
    Nome = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    Senha = models.CharField(max_length=255)
    Matricula = models.CharField(max_length=20, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

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
    questions = models.ManyToManyField(Question, related_name='phases', blank=True)

    def __str__(self):
        return self.name

class Trail(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    phases = models.ManyToManyField(Phase, related_name='trails', blank=True)

    def __str__(self):
        return self.name

class TrailPhase(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.trail} - {self.phase}'

class TrailQuestion(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.trail} - {self.question}'
