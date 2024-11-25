import logging

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import logout
from django.template.defaultfilters import random
from django.http import JsonResponse

from .decorators import professor_required, aluno_required
from .models import Question, Trail, TrailPhase, TrailQuestion
from .forms import ProfessorSignUpForm, AlunoSignUpForm, QuestionForm

logger = logging.getLogger(__name__)

@login_required(login_url='/login')
def home(request):
    if request.user.is_professor:  # Assuming staff users are professors
        return redirect('home-professor')
    else:
        return redirect('home-aluno')

@login_required(login_url='/login')
@aluno_required
def home_aluno(request):
    context = {
        'title': 'Home',
        'buttons': [
            {'name': 'Ranking', 'link': '/ranking'},
            {'name': 'Progresso', 'link': '/progresso'}
        ]
    }

    return render(request, 'home.html', context)

@login_required(login_url='/login')
@professor_required
def home_professor(request):
    context = {
        'title': 'Home',
        'buttons': [
            {'name': 'Gerar Relatorio', 'link': '/relatorio'},
            {'name': 'Cadastrar Perguntas', 'link': '/cadastro_perguntas'},
            {'name': 'Cadastrar Trilha', 'link': '/cadastro_trilha'}
        ]
    }

    return render(request, 'home.html', context)

def cadastro(request):
    context = {
        'title': 'Cadastro',
        'description': 'Escolha o tipo de cadastro',
        'options': [
            {'name': 'Professor', 'link': '/cadastro-professor'},
            {'name': 'Aluno', 'link': '/cadastro-aluno'}
        ],
        'buttons': [
            {'name': 'Login', 'link': '/login'}
        ]
    }
    return render(request, 'cadastro.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f'Usuário: {username}, Senha: {password}')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            print(f'Usuário {user.username} autenticado com sucesso.')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'login.html', {'title': 'Login'})

def cadastro_professor(request):
    if request.method == 'POST':
        form = ProfessorSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('Email')
            nome = form.cleaned_data.get('Nome')
            senha = form.cleaned_data.get('Senha')

            # Check if Email is unique
            if email and get_user_model().objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please choose a different Email.')
            else:
                try:
                    user = get_user_model().objects.create_user(
                        username=email,  # Use Email as username
                        email=email,
                        password=senha,
                        first_name=nome.split()[0],
                        last_name=' '.join(nome.split()[1:]),
                        is_professor=True,
                        Email=email,
                        Nome=nome
                    )
                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    logger.info(f'Professor {user.username} cadastrado com sucesso.')
                    return redirect('home-professor')
                except IntegrityError:
                    messages.error(request, 'An error occurred while creating the user. Please try again.')
    else:
        form = ProfessorSignUpForm()
    return render(request, 'cadastro.html', {
        'title': 'Cadastro Professor',
        'forms': form,
        'options': [
            {'name': 'Cadastrar', 'link': '/cadastro-professor'}
        ],
        'buttons': [
            {'name': 'Login', 'link': '/login'},
            {'name': 'Alterar Cadastro', 'link': '/cadastro'}
        ]
    })

def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('Email')
            matricula = form.cleaned_data.get('Matricula')
            nome = form.cleaned_data.get('Nome')
            senha = form.cleaned_data.get('Senha')

            # Check if Email is unique
            if email and get_user_model().objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please choose a different Email.')
            else:
                try:
                    user = get_user_model().objects.create_user(
                        username=matricula,  # Use Matricula as username
                        email=email,
                        password=senha,
                        first_name=nome.split()[0],
                        last_name=' '.join(nome.split()[1:]),
                        is_aluno=True,
                        Matricula=matricula,
                        Email=email,
                        Nome=nome
                    )
                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    logger.info(f'Aluno {user.username} cadastrado com sucesso.')
                    return redirect('home-aluno')
                except IntegrityError:
                    messages.error(request, 'An error occurred while creating the user. Please try again.')
    else:
        form = AlunoSignUpForm()
    return render(request, 'cadastro.html', {
        'title': 'Cadastro Aluno',
        'forms': form,
        'options': [
            {'name': 'Cadastrar', 'link': '/cadastro-aluno'}
        ],
        'buttons': [
            {'name': 'Login', 'link': '/login'},
            {'name': 'Tipo de Cadastro', 'link': '/cadastro'}
        ]
    })

@login_required(login_url='/login')
@aluno_required
def ranking(request):
    context = {
        'title': 'Ranking',
        'ranking': [
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
            {'name': 'Progresso', 'link': '/progresso'},
            {'name': 'Home', 'link': '/home'}
        ]
    }
    return render(request, 'ranking.html', context)


@login_required(login_url='/login')
@professor_required
def relatorio(request):
    context = {
        'title': 'Relatório',
        'relatorio': [
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
            {'name': 'Home', 'link': '/home'},
            {'name': 'Quiz', 'link': '/quiz'}
        ]
    }
    return render(request, 'relatorio.html', context)

@login_required(login_url='/login')
@aluno_required
def quiz(request):
    context = {
        'title': 'Quiz',
        'questions': [
            {'question': 'Qual a capital do Brasil?', 'answers': ['Brasília', 'Rio de Janeiro', 'São Paulo', 'Curitiba'], 'correct': 0},
            {'question': 'Qual a capital do Acre?', 'answers': ['Brasília', 'Rio Branco', 'São Paulo', 'Curitiba'], 'correct': 1},
        ],
        'buttons': [
            {'name': 'Home', 'link': '/home-aluno'},
            {'name': 'Ranking', 'link': '/ranking'}
        ]
    }
    return render(request, 'quiz.html', context)

@login_required(login_url='/login')
@professor_required
def cadastro_perguntas(request):
    message = None
    message_type = None
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f'Pergunta {form.cleaned_data["question_text"]} cadastrada com sucesso.')
            message = 'Pergunta cadastrada com sucesso.'
            message_type = 'success'
        else:
            message = 'Ocorreu um erro ao cadastrar a pergunta. Por favor, tente novamente.'
            message_type = 'error'
    else:
        form = QuestionForm()
    context = {
        'title': 'Cadastrar Perguntas',
        'form': form,
        'message': message,
        'message_type': message_type,
        'buttons': [
            {'name': 'Home', 'link': '/home-professor'},
            {'name': 'Relatório', 'link': '/relatorio'},
            {'name': 'Editar Trilha', 'link': '/cadastro_trilha'}
        ]
    }
    return render(request, 'cadastro_perguntas.html', context)

def get_questions(request):
    questions = Question.objects.all().values('id', 'text')
    return JsonResponse(list(questions), safe=False)
@login_required(login_url='/login')
@professor_required
def cadastro_trilha(request):
    if request.method == 'POST':
        trail_name = request.POST.get('trail_name')
        trail_description = request.POST.get('trail_description')
        question_mode = request.POST.get('question_mode')
        phases = []

        if question_mode == 'manual':
            for phase_number in range(1, 6):
                phase = []
                for question_number in range(1, 5):
                    question_id = request.POST.get(f'question_{phase_number}_{question_number}')
                    if question_id:
                        try:
                            question = Question.objects.get(id=question_id)
                            phase.append(question)
                        except Question.DoesNotExist:
                            messages.error(request, f'Question with id {question_id} does not exist.')
                            return redirect('cadastro_trilha')
                phases.append(phase)
        else:
            questions = list(Question.objects.all())
            random.shuffle(questions)
            for phase_number in range(1, 6):
                phase = questions[(phase_number-1)*4:phase_number*4]
                phases.append(phase)

        # Save the trail and its phases to the database
        trail = Trail.objects.create(name=trail_name, description=trail_description)
        for phase in phases:
            trail_phase = TrailPhase.objects.create(trail=trail)
            for question in phase:
                TrailQuestion.objects.create(phase=trail_phase, question=question)

        messages.success(request, 'Trilha cadastrada com sucesso.')
        return redirect('home-professor')

    questions = Question.objects.all()
    context = {
        'title': 'Cadastrar Trilha',
        'buttons': [
            {'name': 'Home', 'link': '/home-professor'},
            {'name': 'Relatório', 'link': '/relatorio'},
            {'name': 'Cadastrar Perguntas', 'link': '/cadastro_perguntas'}
        ],
        'questions': questions,
        'range': range(1, 6)
    }
    return render(request, 'cadastro_trilha.html', context)

def get_questions(request):
    questions = Question.objects.all().values('id', 'question_text')
    return JsonResponse(list(questions), safe=False)

def get_question(request):
    question_id = request.GET.get('question_id')
    if question_id:
        try:
            question = Question.objects.get(id=question_id)
            data = {
                'id': question.id,
                'text': question.question_text,
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'option4': question.option4,
                'correct_option': question.correct_option,
                'difficulty': question.difficulty
            }
            return JsonResponse(data)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
    else:
        return JsonResponse({'error': 'No question_id provided'}, status=400)