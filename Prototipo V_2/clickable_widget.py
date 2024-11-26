from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

# Widget genérico que emite sinais quando clicados por botões do mouse. Sinais podem ser usados pra chamar funções
class ClickableWidget(QWidget):
    left_clicked = pyqtSignal(QWidget)
    right_clicked = pyqtSignal(QWidget)
    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: 
            self.left_clicked.emit(self)
        elif event.button() == Qt.RightButton: 
            self.right_clicked.emit(self)