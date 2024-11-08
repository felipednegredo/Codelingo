# Generated by Django 5.1.2 on 2024-11-05 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nome', models.CharField(max_length=100)),
                ('senha', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_professor', models.BooleanField(default=False)),
                ('is_aluno', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='codelingowebapp.usuario')),
                ('codigo', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('codelingowebapp.usuario',),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='codelingowebapp.usuario')),
            ],
            options={
                'abstract': False,
            },
            bases=('codelingowebapp.usuario',),
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField()),
                ('alternativas', models.ManyToManyField(to='codelingowebapp.alternativa')),
            ],
        ),
        migrations.CreateModel(
            name='Trilha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tempo', models.IntegerField()),
                ('tentativas', models.IntegerField()),
                ('titulo', models.CharField(max_length=255)),
                ('valor', models.FloatField()),
                ('perguntas', models.ManyToManyField(to='codelingowebapp.pergunta')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codelingowebapp.professor')),
            ],
        ),
    ]
