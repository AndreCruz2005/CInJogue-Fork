"""
GUI feita com a biblioteca PyQt5
API da Gemini AI: https://aistudio.google.com/app/u/1/apikey
API do GiantBomb: https://www.giantbomb.com/api/
API do TMDB: https://developer.themoviedb.org/reference/intro/authentication
"""
import google.generativeai as genai
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from api_calling import get_game_data, get_movie_data, url_to_png
from color_palette import app_color_palette
import sys, json, requests, random, os

# Checa a existência das pastas de caching
# Obtém o caminho da pasta atual do script
path_to_folder = os.path.dirname(os.path.abspath(__file__))

# Diretórios a serem criados
directories = [
    'caching',
    'caching/images_cache',
    'caching/images_cache/game',
    'caching/images_cache/movie'
]

# Cria os diretórios caso não existam
for dir_name in directories:
    dir_path = os.path.join(path_to_folder, dir_name)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)

# Carregar user data
try:
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {'movie_library': {}, 'game_library': {}, 'movie_recommendations': {'High Priority': {}, 'Low Priority': {}}, 'game_recommendations': {'High Priority': {}, 'Low Priority': {}}}

# Carregar dados de API
try:
    with open('caching/api_data_cache.json', 'r') as file:
        cache = json.load(file)
except FileNotFoundError:
    cache = {'game':{}, 'movie':{}}

# API Keys
GOOGLE_API = "PLACEHOLDER"

# Inicializa Gemini
genai.configure(api_key=GOOGLE_API)

# Configurações do modelo de IA
main_generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",  # Resposta sempre em JSON
}

# Criar o modelo de IA
main_model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=main_generation_config,
  system_instruction=open('model_instructions.txt', encoding="utf8").readlines()
)

# Inicia conversa com o modelo
conversation = main_model.start_chat()

# Função pra adicionar a mensagem do usuário a conversação e retornar a resposta do modelo como texto
def call_ai(prompt):
    response = conversation.send_message(str(prompt))
    return response.text

# Classe para pegar a resposta da IA e APIs em uma thread separada
class AiResponseThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt_full, current_library, current_recommendations, mode):
        super().__init__()
        self.mode = mode
        self.prompt_full = prompt_full
        self.current_library = current_library
        self.current_recommendations = current_recommendations

    def run(self):
        try:
            # Pega a resposta da gemini
            response = call_ai(self.prompt_full)

            # Processar resposta do modelo
            response_list = json.loads(response)
            if type(response_list) != list or False in [(type(item) == dict) for item in response_list]:
                raise Exception(f"Resposta formatada incorretamente: {response}")

            # Para cada comando na lista de respostas
            for response_dictionary in response_list:
                command = response_dictionary.get("command", "")

                # Processa os comandos
                if command == "Recommend":
                    self.current_recommendations['High Priority'], self.current_recommendations['Low Priority']  = {}, {}  # Limpa as recomendações
                    recommendations = response_dictionary.get("recommendations", [])

                    # Para cada recomendação retorna os resultados de busca de acordo com o modo do app
                    for item in recommendations:
                        search_results = get_game_data(item) if self.mode == 'game' else get_movie_data(item)

                        for idx, result in enumerate(search_results):

                            # Alta prioridade == Primeiros resultados de cada pesquisa. Serão exibidos antes dos demais
                            priority = 'High Priority' if idx == 0 else 'Low Priority'

                            # TMDB usa a key 'title' para o nome dos filmes, GiantBomb usa a key 'name' para o nome dos jogos  
                            name_key = 'name' if self.mode == 'game' else 'title'
                            name = result.get(name_key)

                            # Evita adicionar None ao dicionário ou sobrescrever items já adicionados
                            if name is not None and name not in self.current_recommendations[priority] and '/' not in name:
                                self.current_recommendations[priority][name] = result # Adiciona o nome do item associado aos seus dados
                                cache[self.mode][name] = result # Adiciona o resultado ao cache

                                if not os.path.isfile(f"caching/images_cache/{self.mode}/{name}.png"): # Salva a imagem do item no cache
                                    url_to_png(self.mode, result, name)


                elif command == "Add":
                    print(response)
                    additions = response_dictionary.get("additions", [])
                    for item in additions:

                        # Tenta encontrar o item a ser adicionado no cache antes de chamar a API
                        cached_data = cache[self.mode].get(item)
                        if cached_data is not None:
                            name = item
                            data = cached_data
                        else:
                            search_results = get_game_data(item) if self.mode == 'game' else get_movie_data(item)
                            data = search_results[0] # Utiliza o primeiro resultado da pesuisa
                            name_key = 'name' if self.mode == 'game' else 'title'
                            name = data.get(name_key)
                            
                        if name is not None  and '/' not in name:
                            state = f'{'unplayed' if self.mode == 'game' else 'unwatched'}'
                            self.current_library[name] = {'rating':'unrated', 'state': state, 'data': data}
                            cache[self.mode][name] = data
                            if not os.path.isfile(f"caching/images_cache/{self.mode}/{name}.png"):
                                url_to_png(self.mode, data, name)
                
                elif command == "Set_state":
                    new_states = response_dictionary.get("new_states", {})
                    for game, state in new_states.items():
                        if game in self.current_library:
                            self.current_library[game]['state'] = state

                elif command == "Set_rating":
                    new_ratings = response_dictionary.get("new_ratings", {})
                    for game, rating in new_ratings.items():
                        if game in self.current_library:
                            self.current_library[game]['rating'] = rating

                elif command == "Remove":
                    removals = response_dictionary.get("removals", [])
                    for item in removals:
                        if item in self.current_library:
                            del self.current_library[item]
                
            self.finished.emit(response)

        except Exception as e:
            self.error.emit(str(e))

from library_region import LibaryRegion
from ai_recommendations_region import AiRecommendationsRegion

# Janela
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Informações de uso do app
        self.mode = 'game'
        self.user_data = user_data
        # Bibilioteca que será enviada a IA
        self.movie_library = user_data['movie_library']
        self.game_library = user_data['game_library']
        # Resultados de pesquisa associados aos seus dados recolhidos da API com base nas recomendações da IA
        self.movie_recommendations = user_data['movie_recommendations']
        self.game_recommendations = user_data['game_recommendations']
        
        # Botão para trocar o modo do app
        self.switch_button = QPushButton(self)
        self.switch_button.setText("Press me!!")
        self.switch_button.setGeometry(10, 800, 200, 100)
        self.switch_button.pressed.connect(self.switch_mode)
        self.switch_button.setStyleSheet("border: 2px solid white; color: white;")

        self.setStyleSheet(f"background-color: {app_color_palette['dark-medium'][self.mode]}")
        
        #################################
        # GUI
        #################################
        self.center_widget = QWidget(self)
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.center_widget.setLayout(self.hbox)
        self.setCentralWidget(self.center_widget)
        
        # Libary
        self.library_region = LibaryRegion(self)

        # AI
        self.ai_recommendation_region = AiRecommendationsRegion(self)

    # Alterna modo do app entre jogos e filmes
    def switch_mode(self, button_text):
        if button_text == self.mode.upper():
            return
        self.mode = 'game' if self.mode != 'game' else 'movie'

        # Palette changes
        self.setStyleSheet(f"background-color: {app_color_palette['dark-medium'][self.mode]}")
        self.library_region.palette_setting(self.mode)
        self.ai_recommendation_region.palette_setting(self.mode)

        self.library_region.update()
        self.ai_recommendation_region.update()

    def ai_response(self):
        # Take the text in the user input
        prompt = self.ai_recommendation_region.user_chat_input.text()
        self.ai_recommendation_region.user_chat_input.setText('')
        if prompt == "":  # Não enviar prompt vazio
            return
        
        # Formata o prompt de usuário
        current_libarary = self.game_library if self.mode == "game" else self.movie_library
        current_recommendations = self.game_recommendations if self.mode == "game" else self.movie_recommendations
        # Omite os campos de data de cada dicionário para reduzir o tamanho do prompt enviado a IA
        library_for_ai = {key : {'rating':current_libarary[key]['rating'], 'state':current_libarary[key]['state']} for key in current_libarary}
        recom_for_ai = [key for key in current_recommendations['High Priority']] + [key for key in current_recommendations['Low Priority']]
        prompt_full = {'type': self.mode, 'user_prompt': prompt, 'current_library': library_for_ai, 'current_recommendations': recom_for_ai}

        # Pega a resposta da gemini
        self.ai_thread = AiResponseThread(prompt_full, current_libarary, current_recommendations, self.mode)
        self.ai_thread.error.connect(self.handle_error)
        self.ai_thread.finished.connect(self.handle_response)
        self.ai_thread.start()
    
    def clear_recommendations(self):
        # Excluí todas as recomendações do modo atual
        recs = self.game_recommendations if self.mode == 'game' else self.movie_recommendations
        recs['High Priority'], recs['Low Priority'] = {}, {}
        self.ai_recommendation_region.update()

    def load_recommendations(self):
        # Move até 6 recomendações da low priority pra high priority
        recs = self.game_recommendations if self.mode == 'game' else self.movie_recommendations

        amount_to_move = min(len(recs['Low Priority']), 6) 
        new_recs = random.sample([keys for keys in recs['Low Priority']], k=amount_to_move)

        for key in new_recs:
            recs['High Priority'][key] = recs['Low Priority'][key]
            del recs['Low Priority'][key]

        self.ai_recommendation_region.update()

    def handle_response(self, response):
        self.library_region.update()
        self.ai_recommendation_region.update()
            
    def handle_error(self, error):
        print(error)

    def closeEvent(self, event):
        # Salva dados de usuário
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file)

        # Salva o cache
        with open('caching/api_data_cache.json', 'w') as file:
            json.dump(cache, file)

        event.accept()
        sys.exit()

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of main Window
window = MainWindow()
window.showMaximized()

# start the app
sys.exit(App.exec())
