import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

class ProfileEvaluationForm(QWidget):
    # Define a signal that will be emitted when the form is completed
    form_completed = pyqtSignal()

    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.setWindowTitle("Profile Evaluation")
        self.setGeometry(100, 100, 400, 300)

        self.user_data = user_data  # Store reference to shared user_data

        # Layout
        layout = QVBoxLayout()

        # Questions
        self.where_play_label = QLabel("Where do you play games?")
        self.where_play_input = QComboBox()
        self.where_play_input.addItems(["PC", "Console", "Mobile"])

        self.budget_label = QLabel("What is your budget for games?")
        self.budget_input = QLineEdit()

        self.famous_games_label = QLabel("Rate these famous games:")
        self.game_ratings = {
            "EA FC": QSlider(Qt.Horizontal),
            "Call of Duty": QSlider(Qt.Horizontal),
            "Skyrim": QSlider(Qt.Horizontal)
        }

        # Set range for ratings
        for game, slider in self.game_ratings.items():
            slider.setRange(1, 5)
            slider.setTickInterval(1)
            slider.setTickPosition(QSlider.TicksBelow)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        # Add widgets to layout
        layout.addWidget(self.where_play_label)
        layout.addWidget(self.where_play_input)
        layout.addWidget(self.budget_label)
        layout.addWidget(self.budget_input)
        layout.addWidget(self.famous_games_label)

        for game, slider in self.game_ratings.items():
            layout.addWidget(QLabel(f"{game}:"))
            layout.addWidget(slider)

        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_form(self):
        # Update user_data instead of overwriting
        self.user_data["form"]["completed"] = True
        self.user_data["form"]["platforms"] = self.where_play_input.currentText()
        self.user_data["form"]["budget"] = self.budget_input.text()
        self.user_data["form"]["game_ratings"] = {game: slider.value() for game, slider in self.game_ratings.items()}
        
        # Emit the signal when form is completed
        self.form_completed.emit()
        
        # Close the form
        self.close()
