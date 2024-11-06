from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro', views.cadastro, name='cadastro'),

    path('cadastro-professor', views.cadastro_professor, name='cadastro-professor'),

    path('cadastro-aluno', views.cadastro_aluno, name='cadastro-aluno'),
    path('login', views.login, name='login'),

    path('home', views.home, name='home'),
]