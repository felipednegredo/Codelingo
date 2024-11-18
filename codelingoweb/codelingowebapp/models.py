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
    question_text = models.CharField(max_length=200)
    answers = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)

