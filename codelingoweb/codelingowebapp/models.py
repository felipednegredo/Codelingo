from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_professor = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)

    def validar_cadastro(self):
        pass

class Professor(Usuario):
    def gerar_trilha(self, perguntas):
        # Implementação para gerar trilha
        pass

    def validar_trilha(self, trilha_id):
        # Implementação para validar trilha
        pass

class Aluno(Usuario):
    codigo = models.IntegerField()

    def responder_trilha(self, trilha):
        # Implementação para responder trilha
        pass

    def visualizar_trilha(self, trilha):
        # Implementação para visualizar trilha
        pass

class Alternativa(models.Model):
    valor = models.CharField(max_length=255)

class Pergunta(models.Model):
    enunciado = models.TextField()
    alternativas = models.ManyToManyField(Alternativa)

class Trilha(models.Model):
    perguntas = models.ManyToManyField(Pergunta)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    tempo = models.IntegerField()
    tentativas = models.IntegerField()
    titulo = models.CharField(max_length=255)
    valor = models.FloatField()

