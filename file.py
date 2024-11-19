"""
Utiliza a biblioteca PyQt5 para criar a interface de usuário
"""

import google.generativeai as genai
from google.generativeai import caching
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import sys, datetime

genai.configure(api_key="API_KEY_PLACEHOLDER")

# Cache
cache = caching.CachedContent.create(
    model='models/gemini-1.5-flash-8b',
    display_name='cache_base', # used to identify the cache
    system_instruction=(
        "Você deve ajudar o usuário a encontrar os melhores filmes e jogos com base no perfil dele!"
    ),
    ttl=datetime.timedelta(minutes=5),
)

# Inicializa o modelo e a conversação atual
model = genai.GenerativeModel.from_cached_content(cached_content=cache)
conversation = model.start_chat()

# Função pra adicionar a mensagem do usuário a conversação e retornar a resposta do modelo como texto
def call_ai(prompt : str) -> str:
    response = conversation.send_message(prompt)
    return response.text

# Classe para a caixa de input do usuário
class text_input(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setPlaceholderText("Talk to the AI")
        self.setStyleSheet("color: white; background-color: #212121; border: 2px solid white;")

# Classe para mostrar as mensagens enviadas do usuário e do modelo
class chat_label(QLabel):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setWordWrap(True)
        self.setFixedWidth(1366)
        self.setStyleSheet("color: white; background-color: #212121; border: 2px solid white; font-size: 15px;")
        self.setText(text)
        self.adjustSize()
        self.show()

# Janela
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1366, 728)
        self.setStyleSheet("background-color: black;")

        # Widget que conterá as labels com as mensagens da conversação
        self.chat_field = QWidget(self)
        self.chat_field.setFixedWidth(1366)

        # Lista que manterá os objetos das mensagens da conversação
        self.labels = [] 

        # Inicia o campo de input do usuário
        self.input_field = text_input(self)
        self.input_field.setGeometry(0, 650, 1366, 78)
        self.input_field.returnPressed.connect(self.ai_response)  # Chama a função de envio de mensagem quando enter é apertado

    def ai_response(self):
        # Take the text in the user input
        prompt = self.input_field.text()
        if prompt == "":  # Não enviar prompt vazio
            return

        # Criar objeto de mensagem do prompt
        user_label = chat_label(self.chat_field, f"User: {self.input_field.text()}")
        user_label.move(0, self.chat_height())
        self.labels.append(user_label)
        self.input_field.setText("")

        # Pega a resposta da gemini
        response = f"Gemini: {call_ai(prompt)}"

        # Criar objeto de mensagem da resposta
        ai_label = chat_label(self.chat_field, response)
        ai_label.move(0, self.chat_height())
        self.labels.append(ai_label)
        print(response)

        # Atualiza o tamanho do chat field de modo a acomodar todos os objetos de mensagens
        self.chat_field.resize(self.chat_field.width(), sum(label.height() for label in self.labels))

    def chat_height(self):
        # Retorna o y da útlima mensagem no chat para adicionar novas mensagens abaixo
        return self.labels[-1].height() + self.labels[-1].y() if self.labels else 0
    
    def wheelEvent(self, event):
        # Registra o movemento da roda do mouse
        delta = event.angleDelta().y()//8

        # Move as mensagens na tela em resposta a roda do mouse
        self.chat_field.move(self.chat_field.x(), self.chat_field.y() + int(delta))
    

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of main Window
window = MainWindow()
window.show()

# start the app
sys.exit(App.exec())
