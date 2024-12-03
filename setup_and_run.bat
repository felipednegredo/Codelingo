@echo off
echo Configurando o ambiente virtual e instalando dependências...

:: Cria o ambiente virtual
python -m venv env

:: Ativa o ambiente virtual
call .\env\Scripts\activate

:: Instala os pacotes necessários
pip install -r requirements.txt

:: Executa o projeto
python manage.py runserver

:: Mantém o prompt de comando aberto
pause