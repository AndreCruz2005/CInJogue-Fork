
# Gerenciamento de Jogos

## Descrição do Projeto

Uma API desenvolvida para gerenciar jogos utilizando a biblioteca Giant Bomb.

## Estrutura do Projeto

```
api/
│   .env.example          # Exemplo de variáveis de ambiente (template para .env)
│   requeriments.txt      # Dependências da aplicação
│   run.py                # Arquivo principal para rodar a aplicação
│   config.py             # Configurações da aplicação
│
└── app/
    │   __init__.py       # Inicialização do Flask e configuração do banco de dados
    │   models.py         # Definição dos modelos de dados (User, Game)
    │
    ├── routes/           # Rotas da API
    │   │   __init__.py
    │   │   auth_routes.py    # Rotas de autenticação (login e registro)
    │   │   game_routes.py    # Rotas para gerenciamento de jogos
    │
    └── services/
        │   giant_bomb_service.py  # Integração com a API do Giant Bomb
```

### Descrição dos principais componentes:

- **run.py**: Inicializa a aplicação Flask.
- **config.py**: Gerencia as configurações (como banco de dados e variáveis de ambiente).
- **models.py**: Define os modelos `User` e `Game`, utilizados na API.
- **auth_routes.py**: Rotas de autenticação (login e registro de usuários).
- **game_routes.py**: Rotas para listar, adicionar e remover jogos.
- **giant_bomb_service.py**: Serviço responsável por integrar a API do Giant Bomb para buscar informações sobre jogos.

---

## Configuração do Ambiente

1. **Clone o repositório**:

```bash
git clone <url-do-repositorio>
cd api
```

2. **Crie um ambiente virtual**:

```bash
python -m venv venv
source venv/bin/activate   # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**:

```bash
pip install -r requeriments.txt
```

4. **Configuração das variáveis de ambiente**:

Renomeie o arquivo `.env.example` para `.env` e configure suas credenciais, como a chave da API do Giant Bomb e a URL do banco de dados:

```
SECRET_KEY=sua_secret_key
GIANT_BOMB_API_KEY=sua_chave_api
SQLALCHEMY_DATABASE_URI=sqlite:///instance/library.db
```

---

## Como Rodar a API

1. **Execute as migrações para criar as tabelas no banco de dados**:

```bash
flask db upgrade
```

2. **Inicie a aplicação**:

```bash
python run.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

---

## Endpoints Disponíveis

### Autenticação:
- `POST /auth/register`: Registro de usuário.
- `POST /auth/login`: Autenticação do usuário.

### Jogos:
- `GET /games/list`: Lista todos os jogos do usuário
- `POST /games/add`: Adiciona um novo jogo
- `GET /games/search`: Busca um jogo ex /games/search?query=minecraft

---

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **SQLAlchemy**: ORM para gerenciamento do banco de dados.
- **Alembic**: Gerenciamento de migrações.
- **Giant Bomb API**: Para buscar informações sobre jogos.
- **SQLite**: Banco de dados utilizado (local).
