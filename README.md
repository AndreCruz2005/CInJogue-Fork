# CInJogue

## Setup

#### Tenha instalado

- Python 3.13+
- NodeJS 20.17.0+

1. Clone o repositório e navegue para o diretório do projeto:

   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETÓRIO>
   ```

2. Configure as variáveis de ambiente:

   Crie um arquivo .env baseado no .env.example

   ```sh
   cp .env.example .env
   ```

   Edite o arquivo [.env](http://_vscodecontentref_/3) com suas configurações.

### Backend

3. No diretório do projeto, navegue para o diretório do backend:

   ```sh
   cd backend
   ```

4. Crie e ative um ambiente virtual:

   ```sh
   python -m venv .venv
   .venv/Scripts/activate
   ```

5. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

6. Inicie o servidor Flask:
   ```sh
   python flaskr/app.py
   ```

### Frontend

7. No diretório do projeto, navegue para o diretório do frontend:

   ```sh
   cd frontendJS
   ```

8. Instale as dependências:

   ```sh
   npm install
   ```

9. Inicie o servidor de desenvolvimento:
   ```sh
   npm run dev
   ```
10. Acesse o frontend em [http://localhost:8000/](http://localhost:8000/)

## Estrutura do Projeto

- backend: Contém o código do servidor Flask.
- frontendJS: Contém o código do frontend em React.

## Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: Javascript, React, Vite
- **Banco de Dados**: SQLite
