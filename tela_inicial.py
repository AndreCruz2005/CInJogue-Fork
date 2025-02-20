# linguagem: python
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QPushButton, QGroupBox, QRadioButton, QGridLayout, QSizePolicy, QScrollArea, QButtonGroup)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

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
        title = QLabel("Preferências do Usuário")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 50, QFont.Bold))
        title.setStyleSheet("color: #000000;")  # Cor preta
        layout.addWidget(title)

        # Gêneros
        genre_group = QGroupBox("Preferências de Gêneros")
        genre_group.setFont(QFont("Arial", 20, QFont.Bold))
        genre_layout = QGridLayout()
        genres = ["Ação", "Estratégia", "Esportes", "RPG", "Aventura", "Simulação", "Corrida", "Puzzle", "Terror", "Plataforma",
                  "Mundo Aberto", "FPS", "RTS", "MMORPG", "Roguelike", "Stealth", "Survival", "Sandbox", "Metroidvania", "Visual Novel"]
        self.genre_checkboxes = [self.create_check_button(genre) for genre in genres]
        for i, checkbox in enumerate(self.genre_checkboxes):
            genre_layout.addWidget(checkbox, i // 5, i % 5)  # 5 itens por linha
        genre_group.setLayout(genre_layout)
        genre_group.setStyleSheet("color: #000000;")
        layout.addWidget(genre_group)

        # Plataformas
        platform_group = QGroupBox("Plataformas de Jogo")
        platform_group.setFont(QFont("Arial", 20, QFont.Bold))
        platform_layout = QGridLayout()
        platforms = ["PC", "Xbox", "Mobile", "PlayStation", "Nintendo", "VR", "Mac", "Linux", "Stadia", "Switch",
                     "PS5", "PS4", "Xbox Series X", "Xbox One", "Wii U", "3DS", "PS Vita", "Ouya", "Atari", "Sega"]
        self.platform_checkboxes = [self.create_check_button(platform) for platform in platforms]
        for i, checkbox in enumerate(self.platform_checkboxes):
            platform_layout.addWidget(checkbox, i // 5, i % 5)  # 5 itens por linha
        platform_group.setLayout(platform_layout)
        platform_group.setStyleSheet("color: #000000;")
        layout.addWidget(platform_group)

        # Estilo de Jogo
        style_group = QGroupBox("Estilo de Jogo Preferido")
        style_group.setFont(QFont("Arial", 20, QFont.Bold))
        style_layout = QGridLayout()
        styles = ["Multijogador", "Solo", "Coop", "Online", "Offline", "Competitivo", "Casual", "Narrativo", "Exploração", "Puzzle",
                  "Sandbox", "Simulação", "Roguelike", "Stealth", "Survival", "Mundo Aberto", "Plataforma", "Terror", "Visual Novel", "RTS"]
        self.style_checkboxes = [self.create_check_button(style) for style in styles]
        for i, checkbox in enumerate(self.style_checkboxes):
            style_layout.addWidget(checkbox, i // 5, i % 5)  # 5 itens por linha
        style_group.setLayout(style_layout)
        style_group.setStyleSheet("color: #000000;")
        layout.addWidget(style_group)

        # Faixa Etária
        age_group = QGroupBox("Faixa Etária Desejada")
        age_group.setFont(QFont("Arial", 20, QFont.Bold))
        age_layout = QGridLayout()
        ages = ["L", "12", "14", "16", "18"]
        self.age_radiobuttons = [self.create_radio_button(age) for age in ages]
        age_button_group = QButtonGroup(self)
        for i, radiobutton in enumerate(self.age_radiobuttons):
            age_layout.addWidget(radiobutton, i // 5, i % 5)  # 5 itens por linha
            age_button_group.addButton(radiobutton)
        age_group.setLayout(age_layout)
        age_group.setStyleSheet("color: #000000;")
        layout.addWidget(age_group)

        # Orçamento
        budget_group = QGroupBox("Orçamento para Jogos")
        budget_group.setFont(QFont("Arial", 20, QFont.Bold))
        budget_layout = QGridLayout()
        budgets = ["Pagos", "Gratuitos"]
        self.budget_radiobuttons = [self.create_radio_button(budget) for budget in budgets]
        budget_button_group = QButtonGroup(self)
        for i, radiobutton in enumerate(self.budget_radiobuttons):
            budget_layout.addWidget(radiobutton, i // 5, i % 5)  # 5 itens por linha
            budget_button_group.addButton(radiobutton)
        budget_group.setLayout(budget_layout)
        budget_group.setStyleSheet("color: #000000;")
        layout.addWidget(budget_group)

        # Histórico de Jogos
        history_group = QGroupBox("Histórico de Jogos")
        history_group.setFont(QFont("Arial", 20, QFont.Bold))
        history_layout = QVBoxLayout()
        self.history_input = QLineEdit()
        self.history_input.setPlaceholderText("Insira os jogos que você já jogou")
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

    def submit_preferences(self):
        # Coleta as preferências do usuário
        preferences = {
            "genres": {checkbox.text(): checkbox.isChecked() for checkbox in self.genre_checkboxes},
            "platforms": {checkbox.text(): checkbox.isChecked() for checkbox in self.platform_checkboxes},
            "styles": {checkbox.text(): checkbox.isChecked() for checkbox in self.style_checkboxes},
            "age": {radiobutton.text(): radiobutton.isChecked() for radiobutton in self.age_radiobuttons},
            "budget": {radiobutton.text(): radiobutton.isChecked() for radiobutton in self.budget_radiobuttons},
            "history": self.history_input.text()
        }
        print(preferences)  # Aqui você pode processar as preferências conforme necessário

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreferencesForm()
    window.showMaximized()  # Garante que a tela inicie maximizada
    sys.exit(app.exec_())