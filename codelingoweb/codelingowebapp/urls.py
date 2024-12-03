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
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro_perguntas', views.cadastro_perguntas, name='cadastro_perguntas'),
    path('cadastro_trilha', views.cadastro_trilha, name='cadastro_trilha'),
    path('get_questions', views.get_questions, name='get_questions'),
    path('get_question/', views.get_question, name='get_question'),
    path('acessar_trilha/<int:trail_id>/', views.acessar_trilha, name='acessar_trilha'),
    path('participar-trilha/<int:trail_id>/', views.participar_trilha, name='participar_trilha'),
    path('acessar_fase/<int:phase_id>/', views.acessar_fase, name='acessar_fase'),
    path('save-response', views.save_response, name='save_response'),
    path('check_question_exists', views.check_question_exists, name='check_question_exists'),
    path('get_random_questions/<str:difficulty>/', views.get_random_questions, name='get_random_questions'),
]