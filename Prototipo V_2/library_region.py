from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from clickable_widget import ClickableWidget
from color_palette import app_color_palette

# Região à esquerda do app, incluí a caixa da biblioteca e os botões para mudar de modo
class LibaryRegion(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.main_window = parent
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        parent.hbox.addWidget(self, stretch=8)

        # Cabeçalho da area da biblioteca onde ficarão os botões para trocar o modo
        self.library_topbar = QWidget(self)
        self.library_topbar_buttons = {}

        self.library_topbar_layout = QHBoxLayout(self.library_topbar)
        self.library_topbar_layout.setSpacing(0)
        self.library_topbar_layout.setContentsMargins(0, 0, 0, 0)

        # Cria os dois botões de trocar o modo junto na esquerda do layout junto com um label com o título da biblioteca na direita
        for mode_name in ('GAME', 'MOVIE', ''):
            if mode_name != '': # Botões
                button = QPushButton(self.library_topbar)
                button.setText(mode_name + 'S')
                button.setStyleSheet(
                    f"background-color: {app_color_palette['medium' if mode_name == parent.mode.upper() else 'dark-medium'][parent.mode]}; "
                    f"border-top: 3px solid {app_color_palette['medium'][parent.mode]}; border-left: 3px solid {app_color_palette['medium'][parent.mode]}; border-right: 3px solid {app_color_palette['medium'][parent.mode]};"
                    f"color: {app_color_palette['light'][parent.mode]}; "
                    f"font-weight: bold;"
                    f"font-size: 25px;"
                )                
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.pressed.connect(lambda mode_name=button.text()[:-1]: parent.switch_mode(mode_name))
                self.library_topbar_layout.addWidget(button, stretch=1)
                self.library_topbar_buttons[mode_name] = button
            else: # Título
                self.title = QLabel(self)
                self.title.setText(f'MY {parent.mode.upper()} LIBRARY')
                self.title.setAlignment(Qt.AlignCenter)
                self.title.setStyleSheet(f"color: {app_color_palette['light'][parent.mode]}; font-size: 70px; font-weight: bold;")

                self.library_topbar_layout.addWidget(self.title, stretch=7)

        # Adiciona o cabeçalho ao layout com stretch de 1
        self.layout.addWidget(self.library_topbar, stretch=1)
        
        # Cria a area de scroll onde ficarão os filmes e jogos e adiciona ao layout stretch de 8
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"border: 3px solid {app_color_palette['medium'][parent.mode]}")
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.layout.addWidget(self.scroll_area, stretch=8)

        # Widget dentro do scroll com os filmes e jogos
        self.library_content = QWidget(self)
        self.library_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.scroll_area.setWidget(self.library_content)
        self.libary_grid = QGridLayout(self.library_content) # Grid, cada item na grid será os filmes e jogos

        self.update()

    def palette_setting(self, mode):
        # Scroll area
        self.scroll_area.setStyleSheet(f"border: 3px solid {app_color_palette['medium'][mode]}")

        # Botões de troca de modo
        for mode_name in ('GAME', 'MOVIE'):
            self.library_topbar_buttons[mode_name].setStyleSheet(
                    f"background-color: {app_color_palette['medium' if mode_name == mode.upper() else 'dark-medium'][mode]}; "
                    f"border-top: 3px solid {app_color_palette['medium'][mode]}; border-left: 5px solid {app_color_palette['medium'][mode]}; border-right: 3px solid {app_color_palette['medium'][mode]};"
                    f"color: {app_color_palette['light'][mode]}; "
                    f"font-weight: bold;"
                    f"font-size: 25px;"
                )
            
        # Title
        self.title.setStyleSheet(f"color: {app_color_palette['light'][mode]}; font-size: 70px; font-weight: bold;")
        self.title.setText(f'MY {mode.upper()} LIBRARY')

    def update(self):
        # Função para atualizar os filmes e jogos exibidos
        # Apaga todos os items do widget da biblioteca mas não apaga o layout
        for child in self.library_content.children():
            if type(child) != QGridLayout:
                child.deleteLater()

        # Pega o modo atual e o dicionário da biblioteca deste modo na MainWindow
        mode = self.main_window.mode
        library = self.main_window.game_library if mode == 'game' else self.main_window.movie_library

        # Número de items por fileira
        items_per_row = 7  

        # Itera sob o dicionário da biblioteca
        for idx, item in enumerate(library):
            # Extrai o dicionário e o campo de data do diconário
            item_dict = library[item]
            data = item_dict['data']

            # Cria o objeto para exibir este item na biblioteca
            item_displayer = LibraryItemDisplayer(self.library_content, data, mode)
            
            # Configura os elementos do slot da grid de acordo com os dados do item da biblioteca
            item_displayer.image_thumb.setPixmap(QPixmap(f'caching/images_cache/{mode}/{item}.png'))
            item_displayer.title.setText(item)
            item_displayer.rating_bar.setText(item_dict['rating'])
            item_displayer.status_bar.setText(item_dict['state'])

            # Adiciona os items a grid de modo que haja 7 items por fileira
            rows = idx//items_per_row
            collums = idx%items_per_row
            self.libary_grid.addWidget(item_displayer, rows, collums)

        # Preenche a grid da biblioteca com itemdisplayers invisíveis de forma que haja pelo menos 3 fileiras para melhor formatação
        library_size = len(library)
        mininum_for_3_rows = max((items_per_row * 2 + 1) - library_size, 0)
        for i in range(library_size, mininum_for_3_rows+library_size):
            filler = LibraryItemDisplayer(self.library_content, None, mode)
            filler.make_invisible()
            self.libary_grid.addWidget(filler, i//items_per_row, i%items_per_row)

# Classe para mostrar um item na biblioteca com sua imagem, nome, rating e status
class LibraryItemDisplayer(ClickableWidget):
    def __init__(self, parent, data, mode):
        super().__init__(parent)
        self.setFixedSize(166, 280)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Imagem
        self.image_thumb = QLabel(self)
        self.image_thumb.setAlignment(Qt.AlignCenter)
        self.image_thumb.setScaledContents(True)

        # Nome
        self.title = QLabel(self)
        self.title.setStyleSheet(f"font-size:15px;color:{app_color_palette['light'][mode]};background-color:{app_color_palette['medium'][mode]};font-weight:bold;")
        self.title.setAlignment(Qt.AlignCenter)

        # Rating
        self.rating_bar = QLabel(self)
        self.rating_bar.setStyleSheet(f"font-size:15px;color:{app_color_palette['light'][mode]};background-color:{app_color_palette['medium'][mode]}")
        self.rating_bar.setAlignment(Qt.AlignCenter)

        # Status
        self.status_bar = QLabel(self)
        self.status_bar.setStyleSheet(f"font-size:15px;color:{app_color_palette['light'][mode]};background-color:{app_color_palette['medium'][mode]}")
        self.status_bar.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.image_thumb)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.rating_bar)
        self.layout.addWidget(self.status_bar)

    def make_invisible(self):
        self.image_thumb.setStyleSheet("background-color: transparent; border: none;")
        self.title.setStyleSheet("background-color: transparent; border: none;")
        self.rating_bar.setStyleSheet("background-color: transparent; border: none;")
        self.status_bar.setStyleSheet("background-color: transparent; border: none;")