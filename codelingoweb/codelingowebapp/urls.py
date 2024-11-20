from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home-aluno', views.home_aluno, name='home-aluno'),
    path('home-professor', views.home_professor, name='home-professor'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('cadastro-professor', views.cadastro_professor, name='cadastro-professor'),
    path('cadastro-aluno', views.cadastro_aluno, name='cadastro-aluno'),
    path('login', views.login_view, name='login'),
    path('ranking', views.ranking, name='ranking'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('quiz', views.quiz, name='quiz'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro_perguntas', views.cadastro_perguntas, name='cadastro_perguntas'),
]