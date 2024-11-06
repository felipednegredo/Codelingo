from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required(login_url='/login')
def home(request):
    context = {
        'title': 'Home',
        'trails' : [
            { 'name': 'Trilha 1', 'link': '/trilha-1' , 'description': 'Trilha 1 é uma trilha de teste'},
            { 'name': 'Trilha 2', 'link': '/trilha-2' , 'description': 'Trilha 2 é uma trilha de teste'},
            { 'name': 'Trilha 3', 'link': '/trilha-3' , 'description': 'Trilha 3 é uma trilha de teste'},
        ],
        'buttons': [
            {'name': 'Logout', 'link': '/login'},
            {'name': 'Ranking', 'link': '/ranking'},
            {'name': 'Progresso', 'link': '/progresso'}
        ]
    }

    return render(request, 'home.html',context)

def cadastro(request):
    context = {
        'title': 'Cadastro',
        'description': 'Escolha o tipo de cadastro',
        'options' : [
            { 'name': 'Professor', 'link': '/cadastro-professor' },
            { 'name': 'Aluno', 'link': '/cadastro-aluno' }
        ],
        'buttons' : [
            { 'name': 'Login', 'link': '/login' }
        ]
    }
    return render(request, 'cadastro.html',context)

def login(request):
    context = {
        'title': 'Login',
        'forms' : [
            { 'label': 'E-mail', 'type': 'email', 'placeholder': 'Insira o E-mail' },
            { 'label': 'Senha', 'type': 'password', 'placeholder': 'Insira a Senha' },
        ],
        'options' : [
            { 'name': 'Cadastrar', 'link': '/cadastro' },
            { 'name': 'Login', 'link': '/home' }
        ],
        'buttons': []
    }
    return render(request, 'login.html',context)

def cadastro_professor(request):
    context = {
        'title': 'Cadastro Professor',
        'forms' : [
            { 'label': 'Nome', 'type': 'text', 'placeholder': 'Insira o Nome' },
            { 'label': 'E-mail', 'type': 'email', 'placeholder': 'Insira o E-mail' },
            { 'label': 'Senha', 'type': 'password', 'placeholder': 'Insira a Senha' },
        ],
        'options' : [
            { 'name': 'Cadastrar', 'link': '/cadastro-professor' }
        ],
        'buttons': [
            {'name': 'Login', 'link': '/login'},
            {'name': 'Alterar Cadastro', 'link': '/cadastro'}
        ]
    }
    return render(request, 'cadastro.html',context)

def cadastro_aluno(request):
    context = {
        'title': 'Cadastro Aluno',
        'forms' : [
            { 'label': 'Nome', 'type': 'text', 'placeholder': 'Insira o Nome' },
            { 'label': 'E-mail', 'type': 'email', 'placeholder': 'Insira o E-mail' },
            { 'label': 'Matrícula', 'type': 'text', 'placeholder': 'Insira a Matrícula' },
            { 'label': 'Senha', 'type': 'password', 'placeholder': 'Insira a Senha' },
        ],
        'options' : [
            { 'name': 'Cadastrar', 'link': '/cadastro-aluno' }
        ],
        'buttons': [
            {'name': 'Login', 'link': '/login'},
            {'name': 'Tipo de Cadastro', 'link': '/cadastro'}
        ]
    }
    return render(request, 'cadastro.html',context)
