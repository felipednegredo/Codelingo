# Codelingo - Configuração e Execução do Projeto

Bem-vindo ao **Codelingo**, um projeto desenvolvido para a matéria de melhoria de processo de software - (MPS). Siga as instruções abaixo para configurar e executar o ambiente localmente.

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você possui os seguintes itens instalados em sua máquina:

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/) (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

---

## ⚙️ Instruções de Configuração

### 1. Clone o repositório

Clone o repositório para a sua máquina local usando o seguinte comando:

```sh
git clone https://github.com/felipednegredo/Codelingo.git
cd Codelingo
```

---

### 2. Crie e ative um ambiente virtual

Para evitar conflitos de dependências, crie e ative um ambiente virtual:

- **No Windows:**

    ```sh
    python -m venv env
    .\env\Scripts\activate
    ```

- **No macOS/Linux:**

    ```sh
    python -m venv env
    source env/bin/activate
    ```

---

### 3. Instale as dependências

Instale as bibliotecas e pacotes necessários para executar o projeto:

```sh
pip install -r requirements.txt
```

---

### 4. Execute o servidor

Inicie o servidor de desenvolvimento local com o comando:

```sh
python manage.py runserver
```

O servidor estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 🔄 Configuração e Execução Automatizada

Para usuários de **Windows**, um script chamado `setup_and_run.bat` está disponível para automatizar o processo de configuração e execução do projeto.

### Como usar o script automatizado

1. Certifique-se de que o **setup_and_run.bat** está no diretório do projeto.
2. Execute o script no terminal:

    ```sh
    setup_and_run.bat
    ```

O script irá:
- Criar e ativar um ambiente virtual.
- Instalar os pacotes necessários.
- Iniciar o servidor automaticamente.


### 📄 Licença

[Adicione informações sobre a licença, se aplicável, como MIT, Apache, etc.]

---