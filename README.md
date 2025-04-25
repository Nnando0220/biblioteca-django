# Sistema de Gerenciamento de Biblioteca

Este projeto é um sistema de gerenciamento de biblioteca, onde é possível cadastrar, visualizar, atualizar e deletar livros, autores, categorias e coleções. O sistema foi desenvolvido com Django, utilizando o Django REST Framework para criar uma API RESTful.

## Tecnologias Utilizadas
- **Django**: Framework web de alto nível que promove o desenvolvimento rápido e limpo.
- **Django REST Framework**: Ferramenta poderosa para construir APIs web em Django.
- **Django ORM**: Mapeamento objeto-relacional para interagir com o banco de dados.
- **SQLite**: Banco de dados leve e fácil de usar, ideal para desenvolvimento e testes.
- **Coverage**: Ferramenta para medir a cobertura de testes do código.

## Funcionalidades Implementadas

- **CRUD completo** para:
  - Livros
  - Autores
  - Categorias
  - Coleções de livros por usuário

- **Autenticação e Permissões**:
  - Sistema de autenticação baseado em tokens
  - Permissões personalizadas para acesso a recursos
  - Proteção para que usuários só modifiquem suas próprias coleções

- **Recursos da API**:
  - Filtros para pesquisa de livros por título e autor
  - Paginação para grandes conjuntos de resultados
  - Controle de throttling (limite de requisições)
  - Endpoints hiperlinkados para facilitar navegação

- **Integração**:
  - Serialização e deserialização de dados
  - HyperlinkedModelSerializer para relações entre objetos
  - Django ORM para operações com banco de dados

- **Testes**:
  - Testes automatizados com mais de 15 métodos
  - Cobertura de teste de 93%

## Instalação

### Pré-requisitos
- Python 3.8+ 
- pip (gerenciador de pacotes Python)

### Passos para Instalação

#### Windows

```bash
# Clonar o repositório
git clone https://github.com/Nnando0220/biblioteca.git
cd biblioteca

# Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Executar servidor de desenvolvimento
python manage.py runserver
```

#### Linux/MacOS

```bash
# Clonar o repositório
git clone https://github.com/Nnando0220/biblioteca.git
cd biblioteca

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Executar servidor de desenvolvimento
python manage.py runserver
```

## Executando os Testes

### Testes Básicos
Para executar todos os testes do projeto:
```bash
python manage.py test core
```

### Testes Especificos:
Para executar testes de uma classe específica:
```bash
python manage.py test core.tests.LivroTests
```

### Relatórios de Cobertura de Testes:
Instalação do Coverage
```bash
pip install coverage
```

Executando Testes com Cobertura
```bash
# Executar testes com coverage
coverage run manage.py test core

# Gerar relatório no terminal
coverage report

# Gerar relatório HTML (mais detalhado)
coverage html

# Abrir o relatório HTML no navegador
# Windows
start htmlcov/index.html
# Linux
xdg-open htmlcov/index.html
# macOS
open htmlcov/index.html
```

