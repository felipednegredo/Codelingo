import logging
import random
import json
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from .decorators import professor_required, aluno_required
from .models import Question, Trail, Phase, PhaseQuestions, Enrollment, UserResponse, CompletedPhases, TrailPhases
from .forms import ProfessorSignUpForm, AlunoSignUpForm, QuestionForm
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

logger = logging.getLogger(__name__)

@login_required(login_url='/login')
def home(request):
    if request.user.is_teacher:  # Assuming staff users are professors
        return redirect('home-professor')
    else:
        return redirect('home-aluno')

@login_required(login_url='/login')
@aluno_required
def home_aluno(request):
    enrolled_trail = Enrollment.objects.filter(user=request.user).first()
    first_phase_id = None
    if enrolled_trail:
        first_phase = Phase.objects.filter(trailphases__trail=enrolled_trail.trail).order_by('id').first()
        if first_phase:
            first_phase_id = first_phase.id

    trails = Trail.objects.all()
    trails_data = []
    for trail in trails:
        phases_count = TrailPhases.objects.filter(trail=trail).count()
        enrolled_students_count = Enrollment.objects.filter(trail=trail).count()
        trails_data.append({
            'id': trail.id,
            'name': trail.name,
            'description': trail.description,
            'phases_count': phases_count,
            'enrolled_students_count': enrolled_students_count,
            'is_user_enrolled': trail.is_user_enrolled(request.user),
            'first_phase_id': first_phase_id if trail.is_user_enrolled(request.user) else None
        })
    context = {
        'title': 'Home',
        'trails': trails_data,
        'buttons': [
            {'name': 'Ranking', 'link': '/ranking'},
            {'name': 'Progresso', 'link': '/progresso'}
        ]
    }
    return render(request, 'home.html', context)

@login_required(login_url='/login')
@professor_required
def home_professor(request):
    trails = Trail.objects.all()
    trails_data = []
    for trail in trails:
        phases_count = TrailPhases.objects.filter(trail=trail).count()
        enrolled_students_count = Enrollment.objects.filter(trail=trail).count()
        trails_data.append({
            'id': trail.id,
            'name': trail.name,
            'description': trail.description,
            'phases_count': phases_count,
            'enrolled_students_count': enrolled_students_count
        })
    context = {
        'title': 'Home',
        'trails': trails_data,
        'buttons': [
            {'name': 'Gerar Relatorio', 'link': '/relatorio'},
            {'name': 'Cadastrar Perguntas', 'link': '/cadastro_perguntas'},
            {'name': 'Cadastrar Trilha', 'link': '/cadastro_trilha'}
        ]
    }
    return render(request, 'home.html', context)

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redireciona para a página inicial se o usuário já estiver logado
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

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            role = 'aluno' if user.is_student else 'professor' if user.is_teacher else 'unknown'
            return JsonResponse({'success': True, 'role': role})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
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
                        is_teacher=True,
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
                        is_student=True,
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
            {'name': 'Home', 'link': '/home-aluno'}
        ]
    }
    return render(request, 'ranking.html', context)

def acessar_trilha(request, trail_id):
    try:
        trail = Trail.objects.get(id=trail_id)
        phases = Phase.objects.filter(trailphases__trail=trail).order_by('id')
        completed_phases = set(request.user.completedphases_set.values_list('phase_id', flat=True))

        phases_data = []
        for phase in phases:
            phases_data.append({
                'id': phase.id,
                'name': phase.name,
                'description': phase.description,
                'unlocked': phase.id in completed_phases or not phases_data
            })

        context = {
            'trail': trail,
            'phases': phases_data,
            'buttons': [
                {'name': 'Home', 'link': '/home-aluno'},
                {'name': 'Ranking', 'link': '/ranking'}
            ]
        }
        return render(request, 'acessar_trilha.html', context)
    except Trail.DoesNotExist:
        messages.error(request, 'Trilha não encontrada.')
        return redirect('home-aluno')
@login_required(login_url='/login')
@professor_required
def relatorio(request):
    trails = Trail.objects.filter(professor=request.user)
    alunos_data = []

    for trail in trails:
        enrollments = Enrollment.objects.filter(trail=trail)
        for enrollment in enrollments:
            aluno = enrollment.user
            responses = UserResponse.objects.filter(user=aluno, question__phasequestions__phase__trailphases__trail=trail)
            alunos_data.append({
                'id': aluno.id,
                'name': aluno.get_full_name(),
                'trail': trail.name,
                'responses': responses,
                'total_score': sum(response.is_correct for response in responses),
                'total_time': sum(response.response_time for response in responses)
            })

    if request.method == 'POST':
        selected_alunos = request.POST.getlist('alunos')
        selected_data = [aluno for aluno in alunos_data if str(aluno['id']) in selected_alunos]

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.drawString(100, height - 100, "Relatório de Desempenho")
        y = height - 150

        for aluno in selected_data:
            p.drawString(100, y, f"Nome: {aluno['name']}")
            p.drawString(100, y - 20, f"Trilha: {aluno['trail']}")
            p.drawString(100, y - 40, f"Pontuação Total: {aluno['total_score']}")
            p.drawString(100, y - 60, f"Tempo Total: {aluno['total_time']}")
            y -= 100

        p.showPage()
        p.save()
        return response

    context = {
        'title': 'Relatório',
        'alunos': alunos_data,
        'buttons': [
            {'name': 'Home', 'link': '/home-professor'},
            {'name': 'Cadastrar Perguntas', 'link': '/cadastro_perguntas'},
            {'name': 'Editar Trilha', 'link': '/cadastro_trilha'}
        ]
    }
    return render(request, 'relatorio.html', context)

@login_required(login_url='/login')
@professor_required
def cadastro_perguntas(request):
    message = None
    message_type = None
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            if Question.objects.filter(question_text=question_text).exists():
                message = 'A pergunta já existe.'
                message_type = 'error'
            else:
                form.save()
                logger.info(f'Pergunta {question_text} cadastrada com sucesso.')
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
    try:
        questions = list(Question.objects.values('id', 'question_text'))
        return JsonResponse(questions, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='/login')
@professor_required
def cadastro_trilha(request):
    if request.method == 'POST':
        trail_name = request.POST.get('trail_name')
        trail_description = request.POST.get('trail_description')
        question_mode = request.POST.get('question_mode')
        difficulty_level = request.POST.get('difficulty_level')
        phases = []

        if question_mode == 'manual':
            # Manual mode: allow the professor to select questions
            for phase_number in range(1, 6):
                phase = []
                for question_number in range(1, 5):
                    question_id = request.POST.get(f'question_phase_{phase_number}_{question_number}')
                    if question_id:
                        try:
                            question = Question.objects.get(id=question_id)
                            phase.append(question)
                        except Question.DoesNotExist:
                            messages.error(request, f'Question with id {question_id} does not exist.')
                            return redirect('cadastro_trilha')
                phases.append(phase)

        else:  # Aleatório (Random mode)
            difficulty_mapping = {
                'Iniciante': 'easy',
                'Intermediário': 'medium',
                'Avançado': 'hard'
            }
            if difficulty_level:
                questions = list(Question.objects.filter(difficulty=difficulty_mapping[difficulty_level]))
                random.shuffle(questions)
                for phase_number in range(1, 6):
                    phase = questions[(phase_number-1)*4:phase_number*4]
                    phases.append(phase)
            else:
                messages.error(request, 'Nível de dificuldade não selecionado.')
                return redirect('cadastro_trilha')

        # Save the trail and its phases to the database
        trail = Trail.objects.create(name=trail_name, description=trail_description)
        for phase_questions in phases:
            phase = Phase.objects.create(name=f'Phase {phases.index(phase_questions) + 1}', description=f'Description for phase {phases.index(phase_questions) + 1}')
            TrailPhases.objects.create(trail=trail, phase=phase)
            for question in phase_questions:
                if question:  # Verifique se a questão não é nula
                    PhaseQuestions.objects.create(phase=phase, question=question)

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
        'questions_range': range(1, 5),
        'anwers_range': range(1, 5),
        'phases_range': range(1, 6)
    }
    return render(request, 'cadastro_trilha.html', context)


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


@login_required(login_url='/login')
@aluno_required
def participar_trilha(request, trail_id):
    trail = get_object_or_404(Trail, id=trail_id)

    # Check if the user is already enrolled
    if not Enrollment.objects.filter(user=request.user, trail=trail).exists():
        # Enroll the user in the trail
        Enrollment.objects.create(user=request.user, trail=trail)
        messages.success(request, 'Você foi inscrito na trilha com sucesso.')
    else:
        messages.info(request, 'Você já está inscrito nesta trilha.')

    return redirect('acessar_trilha', trail_id=trail.id)

@login_required(login_url='/login')
@aluno_required
def acessar_fase(request, phase_id):
    phase = get_object_or_404(Phase, id=phase_id)
    questions = PhaseQuestions.objects.filter(phase=phase).select_related('question')
    questions_data = []

    for pq in questions:
        question = pq.question
        question_data = {
            'id': question.id,
            'text': question.question_text,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
            'correct_option': question.correct_option,
            'difficulty': question.difficulty
        }
        questions_data.append(question_data)

    context = {
        'phase': phase,
        'questions': questions_data,
        'buttons': [
            {'name': 'Home', 'link': '/home-aluno'},
            {'name': 'Ranking', 'link': '/ranking'}
        ]
    }
    return render(request, 'quiz.html', context)
def check_question_exists(request):
    question_text = request.GET.get('question', '')
    exists = Question.objects.filter(question_text=question_text).exists()
    return JsonResponse({'exists': exists})

@csrf_exempt
def save_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = Question.objects.get(id=data['question_id'])
            is_correct = data['is_correct']
            response_time = data['response_time']
            question_difficulty = data['question_difficulty']
            user_response = UserResponse.objects.create(
                user=request.user,
                question=question,
                is_correct=is_correct,
                response_time=response_time,
                question_difficulty=question_difficulty
            )

            # Check if all questions in the phase are answered
            phase = question.phasequestions_set.first().phase
            total_questions = phase.phasequestions_set.count()
            answered_questions = UserResponse.objects.filter(user=request.user, question__phasequestions__phase=phase).count()

            if answered_questions == total_questions:
                CompletedPhases.objects.create(user=request.user, phase=phase)
                # Unlock the next phase
                next_phase = Phase.objects.filter(trailphases__trail=phase.trailphases_set.first().trail, id__gt=phase.id).first()
                if next_phase:
                    # Logic to unlock the next phase (e.g., notify the user)
                    pass

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error saving response: {e}")
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=500)
    return JsonResponse({'status': 'fail'}, status=400)


logger = logging.getLogger(__name__)


def get_random_questions(request, difficulty):
    if difficulty:
        questions = Question.objects.filter(difficulty=difficulty)[:20]
        questions_list = list(questions)
        logger.debug(f"Fetched {len(questions_list)} questions for difficulty {difficulty}")
        random.shuffle(questions_list)
        phases = [questions_list[i:i + 4] for i in range(0, 20, 4)]
        data = {
            'phases': [{'questions': [{'question_text': q.question_text} for q in phase]} for phase in phases]
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Nível de dificuldade não fornecido'}, status=400)
