# CInJogue

<b>Deployed demo:</b> https://cinjogue.vercel.app/ (lento)

## Índice

1. [Equipe](#equipe)
2. [Projeto](#projeto)
3. [Funcionalidades](#funcionalidades)
   - [Gerenciamento da biblioteca com auxílio da IA](#gerenciamento-da-biblioteca-com-auxílio-da-ia-que-é-capaz-de-5-comandos)
   - [Visualizar a biblioteca de outros usuários e compartilhamento de jogos](#visualizar-a-biblioteca-de-outros-usuários-e-compartilhamento-de-jogos)
   - [Definição de preferências](#definição-de-preferências)
   - [Marcar jogos para que a IA não os recomende novamente](#marcar-jogos-para-que-a-ia-não-os-recomende-novamente)
   - [Obtenção de dados de jogos usando a API do GiantBomb](#obtenção-de-dados-de-jogos-usando-a-api-do-giantbomb)
   - [Interagindo com o modelo de IA](#interagindo-com-o-modelo-de-ia)
4. [Tecnologias Utilizadas](#tecnologias-utilizadas)
   - [Backend](#backend)
   - [Frontend](#frontend)
5. [Estrutura do Projeto](#estrutura-do-projeto)
   - [Diretório `frontendJS`](#diretório-frontendjs)
   - [Diretório `backend`](#diretório-backend)
   - [Diretório `testes`](#diretório-testes)
   - [Arquivos de Configuração](#arquivos-de-configuração)
   - [Outros](#outros)
6. [Instruções para Execução Local](#instruções-para-execução-local)
   - [Requisitos](#requisitos)
   - [Setup](#setup)
     - [Backend](#backend-1)
     - [Frontend](#frontend-1)

## Equipe

Desenvolvimento de Software - CIn/Ufpe - 2024.2 - **Equipe 10**

- André Vinícius Nascimento Cruz - **avnc**
- Gabriel Bezerra Moraes - **gbm2**
- Lavoisier Oliveira Cândido - **loc2**
- Lucas Moraes - **lmo2**
- Lucas Vinicius Moura da Silva - **lvms** (Enviado para a equipe 11)
- Luiz Eduardo de Andrade Lins - **leal** (Recebido da equipe 9)

## Projeto

Aplicação que permite ao usuário criar e gerenciar uma biblioteca pessoal de jogos com assistência do modelo de IA generativa Gemini.

<div align=center>
<img src="screenshots/inuse-library.png"></img>
</div>

## Funcionalidades

### Gerenciamento da biblioteca com auxílio da IA que é capaz de 5 comandos:

| Commando       | Descrição                                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Recomendar     | Exibe jogos com base nas preferências do usuário, estes podem ser adicionados à biblioteca ou recusados pelo usuário.                                              |
| Adicionar      | Adiciona jogos à biblioteca do usuário.                                                                                                                            |
| Classificar    | Define a classificação de items da biblioteca com uma pontuação entre 0 e 10.                                                                                      |
| Definir estado | Define o estado de um item da biblioteca como <b>Não jogado</b>, <b>Jogado</b>, <b>Ainda jogando</b>, <b>Concluído</b>, <b>Abandonado</b>, <b>Lista de desejos</b> |
| Remover        | Remove item da biblioteca                                                                                                                                          |

### Visualizar a biblioteca de outros usuários e compartilhamento de jogos

Clique no ícone de compartilhamento e insira o nome de um usuário na caixa de entrada indicada. Você sera capaz de visualizar os jogos na biblioteca deste. Items que você possui em comum com o outro usuário serão distinguidos com a cor verde. Clique em um item para adiciona-lo à sua prórpira biblioteca.

### Definição de preferências

Clique no ícone de coração, 4 categorias de preferência serão exibidas: Plataforma, gênero, tema e faixa etária. Insira suas preferências relevantes a cada categoria em suas respectivas caixas de entrada o que criará tags para cada uma. Você pode remover as tags clicando nos botões X em cada tag. As preferência serão enviadas ao modelo de IA toda vez que você mandar uma mensagem.

### Marcar jogos para que a IA não os recomende novamente

Clique em um jogo na aba de recomendações da IA e clique no botão não recomende, o título do jogo será adiconado à uma lista que será enviada ao modelo com a instrução explicíta de que aqueles jogos não devem ser recomendados novamente. Você pode visualizar os jogos nessa lista e removê-los dela clicando no ícone de linhas com um X.

### Obtenção de dados de jogos usando a API do [GiantBomb](https://www.giantbomb.com/api/).

Toda vez que a IA tenta adicionar um jogo, seja às recomendações ou à biblioteca, o programa checa se o jogo já foi registrado no banco de dados, caso não, o jogo é procurado através da API de buscas do GiantBomb. Todos os resultados de uma busca são registrados no banco de dados mas somente o primeiro é utilizado para o comando de adição em questão.

### Interagindo com o modelo de IA

Digite seu comando na caixa de entrada no canto inferior direito da tela e envie clicando a tecla ENTER. Exemplos de comandos que você pode experimentar:

    Recomende jogos de ação
    Adicone Minecraft à minha biblioteca
    Coloque a nota de Minecraft como 10
    Adicione 3 jogos de sua escolha à minha biblioteca
    Defina o estado de todos os jogos como Lista de Desejos
    Remova todos os items da minha biblioteca

## Tecnologias Utilizadas

#### **Backend**

- **Python**: Linguagem de programação. Escolhida por já ser familiar aos integrantes do grupo e possuir uma ampla gama de bibliotecas para auxiliar a implemtação das funcionalidades do software.
- **Pytest**: Biblioteca de Python. Utilizada para criação de testes unitários automatizados
- **google.generativeai**: Biblioteca de python. Permite o uso do modelo generativo de linguagem Gemini através de código. Incluindo o envio e recebimento de mensagens, e configurações do formato que as respostas devem seguir.
- **Requests**: Biblioteca de Python. Utilizada para realizar requisições HTTP para a API da GiantBomb e adquirir dados sobre videogames.
- **Flask**: Biblioteca de Python. Usada para criar as rotas de API que permitem que o frontend interaja com o backend, enviando e recebendo informações.
- **SQLAlchemy**: Biblioteca de Python. Utilizada para criação do banco de dados SQLite que armazena todas as informações tanto de jogos quanto de usuários.
- **Speech Recognizer**: Biblioteca de Python. Utilizada para processar as mensagens de voz e enviar elas como texto para o modelo de IA.

#### Frontend

- **HTML**: Linguagem de marcação. Essencial para definir os componentes que estarão presentes na página da aplicação.
- **CSS**: Linguagem de marcação. Essencial para definir como os componentes devem ser exibidos por um navegador.
- **Javascript**: Linguagem de programação. Essencial para criar aplicações interativas que podem ser executadas por um navegador.
- **Node.Js/NPM**: Utilizados para criação da aplicação web e instalação de bibliotecas de Javascript.
- **Vite**: Servidor de desenvolvimento local. Utilizado para execução da aplicação web localmente permitindo o desenvolvimento.
- **React**: Biblioteca de Javascript. Utilizada pois facilita a criação da interface gráfica da aplicação principalmente pelo uso de state hooks que podem ser usados para atualizar as informações exibidas na página em função
  de uma variável de forma automática.
- **Axios**: Biblioteca de Javascript. Utilizada para fazer requisições HTTP ao backend. Escolhida pois possui error handling e JSON parsing automáticos, ao contrário da função nativa de JS fetch().
- **Wav Encoder**: Biblioteca de Javascript. Utilizada para converter o áudio enviado como mensagem de voz para o formato WAV PCM, pois este é o formato reconhecido pela biblioteca Speech Recognizer no backend.

## Estrutura do Projeto

### Diretório `frontendJS`

- **`src/App.jsx`**: Componente principal do frontend que gerencia o estado global da aplicação e renderiza os componentes principais, como biblioteca, chat, e barra lateral.
- **`src/components/auth.jsx`**: Gerencia a autenticação do usuário, incluindo login e cadastro.
- **`src/components/library.jsx`**: Exibe a biblioteca de jogos do usuário, permitindo interações como alterar estado, avaliar e remover jogos.
- **`src/components/chat.jsx`**: Interface para interação com o modelo de IA, incluindo envio de mensagens e gravação de áudio.
- **`src/components/preferences.jsx`**: Permite ao usuário definir preferências relacionadas a plataformas, gêneros, temas e classificações etárias.
- **`src/components/blacklist.jsx`**: Gerencia a lista de jogos que o usuário não deseja receber como recomendação.
- **`src/components/social.jsx`**: Permite visualizar a biblioteca de outros usuários e compartilhar jogos.
- **`src/components/profile-box.jsx`**: Gerencia as configurações de conta do usuário, como alteração de senha e exclusão de conta.
- **`src/styles/`**: Contém os arquivos CSS para estilização dos componentes sendo estes: `App.css`, `library.css`, `chat.css`, `auth.css`, `blacklist.css`, `infobox.css`, `preferences.css`, `profile-box.css` e `social.css`.
- **`index.html`**: Arquivo HTML principal que serve como ponto de entrada para o frontend.
- **`src/global.js`**: Contém configurações globais, como a URL do backend.
- **`package.json`**: Lista de dependências do frontend que devem ser instaladas.

### Diretório `backend`

- **`flaskr/app.py`**: Arquivo principal do backend que inicializa o servidor Flask, o banco de dados com SQLAlchemy e configura as rotas de API.
- **`flaskr/gemini/gemini.py`**: Implementa a integração com o modelo de IA Gemini, incluindo as instruções e configurações do modelo.
- **`flaskr/giantbomb/giantbomb.py`**: Implementa a integração com a API de busca do GiantBomb.
- **`flaskr/routes/`**: Contém os arquivos que definem as rotas específicas da API, como autenticação, gerenciamento de
  biblioteca e preferências.
- **`flaskr/database/`**: Gerencia a interação com o banco de dados SQLite, incluindo modelos e operações CRUD.
- **`requirements.txt`**: Lista de dependências do backend que devem ser instaladas.

### Diretório `testes`

- **`tests/conftest.py`**: Configurações globais para os testes, incluindo a criação de fixtures para inicializar o banco de dados em memória e criar usuários de teste.
- **`tests/test_users.py`**: Testa funcionalidades relacionadas a usuários, como login, alteração de senha e remoção de conta.
- **`tests/test_tags.py`**: Testa a adição, remoção e recuperação de preferências do usuário.
- **`tests/test_recommendations.py`**: Testa a funcionalidade de recomendações, incluindo a remoção de jogos das recomendações.
- **`tests/test_library.py`**: Testa operações relacionadas à biblioteca do usuário, como adicionar, remover, atualizar estado e avaliar jogos.
- **`tests/test_blacklist.py`**: Testa a funcionalidade da lista de não recomende, incluindo adicionar e remover jogos da lista.
- **`tests/test_ai.py`**: Testa a interação com o modelo de IA, verificando os comandos como recomendar, adicionar, remover, avaliar e alterar estado de jogos. Não verifica o conteúdo mas sim a estrutura das respostas, uma vez que o conteúdo é variável. Falhas nesses testes indicariam de a necessidade instruções mais robustas para o modelo generativo.

### Arquivos de Configuração

- **`.env.example`**: Exemplo de arquivo de configuração de variáveis de ambiente, como chaves de API.
- **`setup.sh`**: Script para configurar e iniciar o backend e frontend automaticamente.
- **`.prettierrc.yaml`**: Arquivo de configurações para formatação automática do código no VSCode com a extensão Prettier.

### Outros

- **`ROTAS.md`**: Documentação detalhada das rotas da API do backend, incluindo exemplos de requisições e respostas.
- **`screenshots/`**: Contém capturas de tela da aplicação, ilustrando suas capacidades.

## Instruções para Execução Local

### Requisitos

- [Python 3.13](https://www.python.org/downloads/) ou mais recente
- [Node.js 20.17.0](https://nodejs.org/en/download) ou mais recente
- Chave de API do [Gemini AI](https://aistudio.google.com/app/apikey)
- Chave de API do [GiantBomb](https://www.giantbomb.com/api/)

**OBS:** Será necessário criar contas em cada uma das plataformas para conseguir uma chave de API.

### Setup

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

3. Tendo configurado o arquivo .env, execute o arquivo setup.sh em um terminal bash para configurar e iniciar o backend
   e frontend
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
