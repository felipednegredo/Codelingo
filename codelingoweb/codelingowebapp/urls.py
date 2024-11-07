from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro', views.cadastro, name='cadastro'),

    path('cadastro-professor', views.cadastro_professor, name='cadastro-professor'),

    path('cadastro-aluno', views.cadastro_aluno, name='cadastro-aluno'),
    path('login', views.login, name='login'),

    path('home', views.home, name='home'),

    path('ranking', views.ranking, name='ranking'),

    path('relatorio', views.relatorio, name='relatorio'),

    path('quiz', views.quiz, name='quiz'),

    path('cadastro-perguntas', views.cadastro_perguntas, name='cadastro-perguntas'),
]