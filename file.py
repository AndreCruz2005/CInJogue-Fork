import google.generativeai as genai
from google.generativeai import caching
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import sys, datetime

genai.configure(api_key="AIzaSyAGXnQtI-EKxrKwgWXDP7lwV-Zc6udbL8M")

# Cache
cache = caching.CachedContent.create(
    model='models/gemini-1.5-flash-8b',
    display_name='bjorn', # used to identify the cache
    system_instruction=(
        "Você deve ajudar o usuário a encontrar os melhores filmes e jogos com base no perfil dele!"
    ),
    ttl=datetime.timedelta(minutes=5),
)

# Initialize the model and the conversation
model = genai.GenerativeModel.from_cached_content(cached_content=cache)
conversation = model.start_chat()

def call_ai(prompt : str) -> str:
    response = conversation.send_message(prompt)
    return response.text

class text_input(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setPlaceholderText("Talk to the AI")
        self.setStyleSheet("color: white; background-color: #212121; border: 2px solid white;")

class chat_label(QLabel):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setWordWrap(True)
        self.setFixedWidth(1366)
        self.setStyleSheet("color: white; background-color: #212121; border: 2px solid white; font-size: 15px;")
        self.setText(text)
        self.adjustSize()
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1366, 728)
        self.setStyleSheet("background-color: black;")

        # Field and list for chat labels
        self.chat_field = QWidget(self)
        self.chat_field.setFixedWidth(1366)
        self.labels = []

        # Init the user input field
        self.input_field = text_input(self)
        self.input_field.setGeometry(0, 650, 1366, 78)
        self.input_field.returnPressed.connect(self.ai_response)

    def ai_response(self):
        # Take the text in the user input
        prompt = self.input_field.text()

        # Create chat label for the user prompt
        user_label = chat_label(self.chat_field, f"User: {self.input_field.text()}")
        user_label.move(0, self.chat_height())
        self.labels.append(user_label)
        self.input_field.setText("")

        # Get the response from gemini
        response = f"Gemini: {call_ai(prompt)}"

        # Create chat label for the ai response
        ai_label = chat_label(self.chat_field, response)
        ai_label.move(0, self.chat_height())
        self.labels.append(ai_label)
        print(response)

        self.chat_field.resize(self.chat_field.width(), sum(label.height() for label in self.labels))

    def chat_height(self):
        # Return the y below the last chat label
        return self.labels[-1].height() + self.labels[-1].y() if self.labels else 0
    
    def wheelEvent(self, event):
        # Get the number of degrees the wheel was rotated
        delta = event.angleDelta().y()//8

        # Scroll through the chat messages
        self.chat_field.move(self.chat_field.x(), self.chat_field.y() + int(delta))
    

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = MainWindow()
window.show()

# start the app
sys.exit(App.exec())
