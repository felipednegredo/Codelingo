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
            {'name': 'Login', 'link': '/home'},
            { 'name': 'Cadastrar', 'link': '/cadastro' },
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

def ranking(request):
    context = {
        'title': 'Ranking',
        'ranking' : [
            {'name': 'Aluno 1', 'score': 100, 'id': 1},
            {'name': 'Aluno 2', 'score': 90, 'id': 2},
            {'name': 'Aluno 3', 'score': 80, 'id': 3},
            {'name': 'Aluno 4', 'score': 70, 'id': 4},
            {'name': 'Aluno 5', 'score': 60, 'id': 5},
            {'name': 'Aluno 6', 'score': 50, 'id': 6},
            {'name': 'Aluno 7', 'score': 40, 'id': 7},
            {'name': 'Aluno 8', 'score': 30, 'id': 8},
            {'name': 'Aluno 9', 'score': 20, 'id': 9},
            {'name': 'Aluno 10', 'score': 10, 'id': 10},
        ],
        'buttons': [
            {'name': 'Logout', 'link': '/login'},
            {'name': 'Progresso', 'link': '/progresso'},
            {'name': 'Home', 'link': '/home'}
        ]
    }
    return render(request, 'ranking.html',context)

def relatorio(request):
    context = {
        'title': 'Relatório',
        'relatorio' : [
            {'name': 'Aluno 1', 'score': 100, 'id': 1},
            {'name': 'Aluno 2', 'score': 90, 'id': 2},
            {'name': 'Aluno 3', 'score': 80, 'id': 3},
            {'name': 'Aluno 4', 'score': 70, 'id': 4},
            {'name': 'Aluno 5', 'score': 60, 'id': 5},
            {'name': 'Aluno 6', 'score': 50, 'id': 6},
            {'name': 'Aluno 7', 'score': 40, 'id': 7},
            {'name': 'Aluno 8', 'score': 30, 'id': 8},
            {'name': 'Aluno 9', 'score': 20, 'id': 9},
            {'name': 'Aluno 10', 'score': 10, 'id': 10},
        ],
        'buttons': [
            {'name': 'Logout', 'link': '/login'},
            {'name': 'Home', 'link': '/home'}
        ]
    }
    return render(request, 'relatorio.html',context)

def quiz(request):
    context = {
        'title': 'Quiz',
        'questions' : [
            {'question': 'Qual a capital do Brasil?', 'answers': ['Brasília', 'Rio de Janeiro', 'São Paulo', 'Curitiba'], 'correct': 0},
            {'question': 'Qual a capital do Acre?', 'answers': ['Brasília', 'Rio Branco', 'São Paulo', 'Curitiba'], 'correct': 1},
        ],
        'buttons': [
            {'name': 'Logout', 'link': '/login'},
            {'name': 'Home', 'link': '/home'}
        ]
    }
    return render(request, 'quiz.html',context)

def cadastro_perguntas(request):
    context = {
        'title': 'Cadastrar Perguntas',
        'buttons': [
            {'name': 'Logout', 'link': '/login'},
            {'name': 'Home', 'link': '/home'}
        ]
    }
    return render(request, 'cadastro_perguntas.html',context)
