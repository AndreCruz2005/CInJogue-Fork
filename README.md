# CInJogue

## Setup

### Tenha instalado

- Python 3.13+
- NodeJS 20.17.0+

1. Clone o repositório:
   ```sh
   git clone <URL_DO_REPOSITORIO>
   ```

### Backend

2. Navegue até o diretório do projeto:

   ```sh
   cd CIN0136
   ```

3. Crie e ative um ambiente virtual:

   ```sh
   python -m venv backend/.venv
   backend/.venv/Scripts/activate
   ```

4. Instale as dependências:

   ```sh
   pip install -r backend/requirements.txt
   ```

5. Configure as variáveis de ambiente:

   - Crie um arquivo [.env](http://_vscodecontentref_/1) baseado no [.env.example](http://_vscodecontentref_/2):
     ```sh
     cp .env.example .env
     ```
   - Edite o arquivo [.env](http://_vscodecontentref_/3) com suas configurações.

6. Inicie o servidor Flask:
   ```sh
   python backend\flaskr\app.py
   ```

### Frontend

7. Navegue até o diretório do frontend:

   ```sh
   cd ../frontendJS
   ```

8. Instale as dependências:

   ```sh
   npm install
   ```

9. Inicie o servidor de desenvolvimento:
   ```sh
   npm run dev
   ```
10. Acesse o frontend em

    [http://localhost:8000/](http://localhost:8000/)

## Estrutura do Projeto

- [backend](http://_vscodecontentref_/4): Contém o código do servidor Flask.
- [frontendJS](http://_vscodecontentref_/5): Contém o código do frontend em React.
- [migrations](http://_vscodecontentref_/6): Contém os arquivos de migração do banco de dados.

## Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: Javascript, React, Vite
- **Banco de Dados**: SQLite
