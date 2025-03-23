# linguagem: python
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QPushButton, QGroupBox, QRadioButton, QGridLayout, QSizePolicy, QScrollArea, QButtonGroup)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import json
import os
from app_function_data import path_to_folder
from main import call_ai, MainWindow  # Importa a função call_ai e a classe MainWindow do main.py

user_data_path = os.path.join(path_to_folder, 'user_preferences.json')


try:
    with open(user_data_path, 'r') as file:
        user_preferences = json.load(file)
        if not user_preferences:  # Verifica se o JSON está vazio
            raise ValueError("JSON vazio")
except (FileNotFoundError, ValueError, json.JSONDecodeError):
    user_preferences = {
            "done": False,
            "genres":{},
            "platforms":[],
            "styles": [],
            "age": [],
            "budget": [],
            "history": ""
    }


class PreferencesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preferências do Usuário")
        self.setStyleSheet("background-color: #ADD8E6;")  # Fundo azul claro
        self.initUI()
        self.showMaximized()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Widget de conteúdo para o scroll area
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título
        title = QLabel("Definas suas preferências")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 50, QFont.Bold))
        title.setStyleSheet("color: #000000;")
        layout.addWidget(title)

        # Função auxiliar para criar um grupo com "Selecionar Todos"
        def create_checkbox_group(group_title, items, columns=5):
            group = QGroupBox(group_title)
            group.setFont(QFont("Arial", 20, QFont.Bold))
            grid = QGridLayout()
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setSpacing(10)
            # "Selecionar Todos" ocupa uma linha completa
            select_all = QCheckBox("Selecionar Todos")
            select_all.setStyleSheet("""
                QCheckBox {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 2px solid #000000;
                    border-radius: 15px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 18px;
                }
                QCheckBox::indicator {
                    width: 0px;
                    height: 0px;
                }
                QCheckBox::checked {
                    background-color: #007BFF;
                    color: white;
                    border: 4px solid #0056b3;
                }
            """)
            grid.addWidget(select_all, 0, 0, 1, columns)
            # Cria uma lista de checkboxes para os itens
            boxes = [self.create_check_button(item) for item in items]
            for i, box in enumerate(boxes):
                row = 1 + i // columns
                col = i % columns
                grid.addWidget(box, row, col)
            # Conecta o "Selecionar Todos" para marcar/desmarcar todos
            select_all.stateChanged.connect(lambda state, b=boxes: [cb.setChecked(state == Qt.Checked) for cb in b])
            group.setLayout(grid)
            group.setStyleSheet("color: #000000;")
            return group, boxes

        # Gêneros
        genres = ["Ação", "Estratégia", "Esportes", "RPG", "Aventura", "Simulação", "Corrida", "Puzzle", "Terror", "Plataforma",
                  "Mundo Aberto", "FPS", "RTS", "MMORPG", "Roguelike", "Stealth", "Survival", "Sandbox", "Metroidvania", "Visual Novel"]
        genre_group, self.genre_checkboxes = create_checkbox_group("Preferências de Gêneros", genres)
        layout.addWidget(genre_group)

        # Plataformas
        platforms = ["PC", "Xbox", "Mobile", "PlayStation", "Nintendo", "VR", "Mac", "Linux", "Stadia", "Switch",
                     "PS5", "PS4", "Xbox Series X", "Xbox One", "Wii U", "3DS", "PS Vita", "Ouya", "Atari", "Sega"]
        platform_group, self.platform_checkboxes = create_checkbox_group("Plataformas de Jogo", platforms)
        layout.addWidget(platform_group)

        # Estilo de Jogo
        styles = ["Multijogador", "Solo", "Coop", "Online", "Offline", "Competitivo", "Casual", "Narrativo", "Exploração", "Puzzle",
                  "Sandbox", "Simulação", "Roguelike", "Stealth", "Survival", "Mundo Aberto", "Plataforma", "Terror", "Visual Novel", "RTS"]
        style_group, self.style_checkboxes = create_checkbox_group("Estilo de Jogo Preferido", styles)
        layout.addWidget(style_group)

        # Faixa Etária (permanece com botões de rádio)
        age_group = QGroupBox("Faixa Etária Desejada")
        age_group.setFont(QFont("Arial", 20, QFont.Bold))
        age_layout = QGridLayout()
        ages = ["L", "12", "14", "16", "18"]
        self.age_radiobuttons = [self.create_radio_button(age) for age in ages]
        age_button_group = QButtonGroup(self)
        for i, radiobutton in enumerate(self.age_radiobuttons):
            age_layout.addWidget(radiobutton, i // 5, i % 5)
            age_button_group.addButton(radiobutton)
        age_group.setLayout(age_layout)
        age_group.setStyleSheet("color: #000000;")
        layout.addWidget(age_group)

        # Orçamento - Alterado para checkboxes para permitir selecionar ambos
        budget_group = QGroupBox("Orçamento para Jogos")
        budget_group.setFont(QFont("Arial", 20, QFont.Bold))
        budget_layout = QGridLayout()
        budgets = ["Pagos", "Gratuitos"]
        self.budget_checkboxes = [self.create_check_button(budget) for budget in budgets]
        for i, checkbox in enumerate(self.budget_checkboxes):
            budget_layout.addWidget(checkbox, i // 5, i % 5)
        budget_group.setLayout(budget_layout)
        budget_group.setStyleSheet("color: #000000;")
        layout.addWidget(budget_group)

        # Histórico de Jogos
        history_group = QGroupBox("Histórico de Jogos")
        history_group.setFont(QFont("Arial", 20, QFont.Bold))
        history_layout = QVBoxLayout()
        self.history_input = QLineEdit()
        self.history_input.setPlaceholderText("Insira os jogos que você já jogou")
        self.history_input.setFont(QFont("Arial", 24))
        history_layout.addWidget(self.history_input)
        history_group.setLayout(history_layout)
        history_group.setStyleSheet("color: #000000;")
        layout.addWidget(history_group)

        # Botão de Enviar
        self.submit_button = QPushButton("Enviar")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                font-weight: bold;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.submit_button.clicked.connect(self.submit_preferences)
        self.submit_button.clicked.connect(self.save_preferences)
        layout.addWidget(self.submit_button)

    def create_check_button(self, text):
        button = QCheckBox(text)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setStyleSheet("""
            QCheckBox {
                background-color: #FFFFFF;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
                font-size: 18px;
            }
            QCheckBox::indicator {
                width: 0px;
                height: 0px;
            }
            QCheckBox::checked {
                background-color: #007BFF;
                color: white;
                border: 4px solid #0056b3;
            }
        """)
        return button

    def create_radio_button(self, text):
        button = QRadioButton(text)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setStyleSheet("""
            QRadioButton {
                background-color: #FFFFFF;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
                font-size: 18px;
            }
            QRadioButton::indicator {
                width: 0px;
                height: 0px;
            }
            QRadioButton::checked {
                background-color: #007BFF;
                color: white;
                border: 4px solid #0056b3;
            }
        """)
        return button

    def preferences(self):
        # Coleta as preferências do usuário
        preferences = {
            "done": True,
            "genres": [checkbox.text() for checkbox in self.genre_checkboxes if checkbox.isChecked()],
            "platforms": [checkbox.text() for checkbox in self.platform_checkboxes if checkbox.isChecked()],
            "styles": [checkbox.text() for checkbox in self.style_checkboxes if checkbox.isChecked()],
            "age": [radiobutton.text() for radiobutton in self.age_radiobuttons if radiobutton.isChecked()],
            "budget": [checkbox.text() for checkbox in self.budget_checkboxes if checkbox.isChecked()],
            "history": self.history_input.text()
        }
        print(preferences)  # Aqui você pode processar as preferências conforme necessário
        return preferences
    

    def submit_preferences(self):
        # Envia as preferências para a IA
        preferences = self.preferences()
        response = call_ai(json.dumps(preferences))
        print(response)  # Exibe a resposta da IA



    def save_preferences(self):
        preferences = self.preferences()
        with open(user_data_path, 'w') as file:
            json.dump(preferences, file, indent=4)

        # Abre a tela principal com as preferências escolhidas
        self.main_window = MainWindow()
        self.main_window.showMaximized()

        # Fecha a tela inicial
        self.close()
if __name__ == "__main__":

    app = QApplication(sys.argv)
    if not user_preferences["done"]:
        window = PreferencesForm()
    else:
        window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())

