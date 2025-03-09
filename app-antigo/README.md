# Projeto de Biblioteca de Jogos com Recomendação de IA

## Visão Geral

Este projeto é uma aplicação de gerenciamento de biblioteca de jogos que utiliza a API da Gemini AI para fornecer recomendações de jogos. A interface gráfica foi construída inicialmente usando PyQt5.

## Estrutura do Projeto e Descrição dos Arquivos e Diretórios

- **ai_recommendations_region.py**: Contém a classe AiRecommendationsRegion que gerencia a área de recomendações da IA na interface.
- **api_calling.py**: Contém funções para chamadas de API, como get_game_data e url_to_png.
- **app_function_data.py**: Contém dados e funções auxiliares, como a paleta de cores do aplicativo.
- **assets/**: Diretório para armazenar recursos estáticos, como imagens.
- **caching/**: Diretório para armazenar dados em cache, incluindo imagens e dados de API.
- **library_region.py**: Contém a classe LibraryRegion que gerencia a área da biblioteca de jogos na interface.
- **LICENSE**: Arquivo de licença do projeto.
- **main.py**: Arquivo principal que inicializa a aplicação e gerencia a lógica principal.
- **model_instructions.txt**: Instruções para o modelo de IA.
- **README.md**: Arquivo de documentação do projeto.
- **requirements.txt**: Lista de dependências do projeto.
- **user_data.json**: Arquivo que armazena os dados do usuário.
- **venv/**: Diretório do ambiente virtual Python.

## Instalação

### Pré-requisitos

- Python 3.13 ou superior
- Ambiente virtual Python (recomendado)

### Passos para Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/Lavoisier-Oliveira/CIN0136.git
    cd CIN0136
    ```

2. Crie e ative um ambiente virtual:
    ```sh
    python -m venv venv
    # seguido de
    source venv/bin/activate # Linux
    # ou
    venv\Scripts\activate # Windows
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

### Executando a Aplicação

Para iniciar a aplicação, execute o seguinte comando no terminal:
```sh
python main.py
```

### Funcionalidades

- **Biblioteca de Jogos**: Gerencie sua biblioteca de jogos, incluindo adicionar, remover e visualizar jogos.
- **Recomendações de IA**: Receba recomendações de jogos com base em suas preferências e biblioteca atual.
- **Interface Gráfica**: Interface amigável construída com PyQt5.
## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.