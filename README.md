# CInJogue

<b>Deployed demo:</b> https://cinjogue.vercel.app/ (lento)

Aplicação que permite ao usuário criar e gerenciar uma biblioteca pessoal de jogos com assistência do modelo de IA
generativa Gemini.

<div align=center>
<a href="https://ibb.co/Kxk6zVqt"><img src="https://i.ibb.co/hFjs12WG/Screenshot-2025-03-08-at-18-08-59-CIn-Jogue.png" alt="Screenshot-2025-03-08-at-18-08-59-CIn-Jogue" border="0" /></a>
</div>

## Funcionalidades

Obtenção de dados de jogos usando a API do [GiantBomb](https://www.giantbomb.com/api/).

Gerenciamento da biblioteca interagindo com a IA que é capaz de 5 comandos:

- Recomendar: Exibe jogos com base nas preferências do usuário, estes podem ser adicionados à biblioteca ou recusados
  pelo usuário.
- Adicionar: Adiciona jogos à biblioteca do usuário
- Classificar: Define a classificação de items da biblioteca com uma pontuação entre 0 e 10.
- Definir estado: Define o estado de um item da biblioteca como <b>Não jogado</b>, <b>Jogado</b>, <b>Ainda jogando</b>,
  <b>Concluído</b>, <b>Abandonado</b>, <b>Lista de desejos</b>
- Remover: Remove item da biblioteca

Definição de preferências relacionadas à plataformas, gêneros, temas e faixas etárias com um sistema de tags cridas pelo
usuário.

Marcar jogos para que a IA não os recomende novamente

## Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: Javascript, React, Vite
- **Banco de Dados**: SQLite

## Estrutura do Projeto

#### Backend (Servidor em Flask e database com SQLAlchemy e SQLite)

```
├── backend/
│   ├── flaskr/
│   │   ├── app.py
│   │   ├── database/
│   │   ├── gemini/
│   │   ├── giantbomb/
│   │   ├── routes/
│   ├── tests/
│   ├── requirements.txt
```

#### Frontend (Aplicação web feita com React + Vite)

```
├── frontendJS/
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── node_modules/
│   ├── package.json
│   ├── package-lock.json
│   ├── public/
│   ├── src/
│   │   ├── Assets/
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── global.js
│   │   ├── main.jsx
│   │   ├── styles/
│   ├── vite.config.js
```

## Requisitos

- [Python 3.13](https://www.python.org/downloads/) ou mais recente
- [Node.js 20.17.0](https://nodejs.org/en/download) ou mais recente
- Chave de API do [Gemini AI](https://aistudio.google.com/app/apikey)
- Chave de API do [GiantBomb](https://www.giantbomb.com/api/)

**OBS:** Será necessário criar contas em cada uma das plataformas para conseguir uma chave de API.

## Setup

1. Clone o repositório e navegue para o diretório do projeto:

   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETÓRIO>
   ```

2. Configure as variáveis de ambiente:

   Crie um arquivo .env baseado no .env.example

   ```sh
   copy .env.example .env
   ```

   Edite o arquivo .env com suas configurações.

3. Tendo configurado o arquivo .env, execute o arquivo setup.sh em um terminal bash para configurar e iniciar o backend e frontend
   ```
   chmod +x setup.sh
   ./setup.sh
   ```
   Alternativamente, siga os próximos passos para configurar e iniciar o projeto manualmente

### Backend

1. No diretório do projeto, navegue para o diretório do backend:

   ```sh
   cd backend
   ```

2. Crie e ative um ambiente virtual:

   ```sh
   python -m venv .venv
   .venv/Scripts/activate
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

4. Inicie o servidor Flask:
   ```sh
   python flaskr/app.py
   ```

### Frontend

1. No diretório do projeto, navegue para o diretório do frontend:

   ```sh
   cd frontendJS
   ```

2. Instale as dependências:

   ```sh
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```sh
   npm run dev
   ```
4. Acesse o frontend em [http://localhost:8000/](http://localhost:8000/)

## Equipe

- André Cruz
- Gabriel Bezerra Moraes
- Lavoisier Oliveira Cândido
- Lucas Moraes
- Lucas Vinicius Moura da Silva
- Luiz Eduardo de Andrade Lins
