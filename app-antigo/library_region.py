from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from app_function_data import app_color_palette, path_to_folder, os

# Região à esquerda do app, incluí a caixa da biblioteca
class LibraryRegion(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        parent.hbox.addWidget(self, stretch=8)

        # Cabeçalho da área da biblioteca
        self.library_topbar = QWidget(self)
        self.library_topbar_layout = QHBoxLayout(self.library_topbar)
        self.library_topbar_layout.setSpacing(0)
        self.library_topbar_layout.setContentsMargins(0, 0, 0, 0)

        # Label com o título da biblioteca
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.library_topbar_layout.addWidget(self.title, stretch=1)

        # Adiciona o cabeçalho ao layout com stretch de 1
        self.layout.addWidget(self.library_topbar, stretch=1)
        
        # Cria a área de scroll onde ficarão os jogos e adiciona ao layout stretch de 8
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.layout.addWidget(self.scroll_area, stretch=8)

        # Widget dentro do scroll com os jogos
        self.library_content = QWidget(self)
        self.library_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.scroll_area.setWidget(self.library_content)
        self.libary_grid = QGridLayout(self.library_content) # Grid, cada item na grid será os jogos

        self.palette_setting(self.parent.mode)
        self.update()

    def palette_setting(self, mode):
        # Scroll area
        self.scroll_area.setStyleSheet(f"border: 3px solid {app_color_palette['medium'][mode]}")

        # Title
        self.title.setStyleSheet(f"color: {app_color_palette['light'][mode]}; font-size: 60px; font-weight: bold;")
        self.title.setText("MINHA BIBLIOTECA DE JOGOS")

    def update(self):
        # Função para atualizar os jogos exibidos
        # Apaga todos os items do widget da biblioteca resetando-a, mas não apaga o layout
        for child in self.library_content.children():
            if type(child) != QGridLayout:
                child.deleteLater()

        # Pega o modo atual e o dicionário da biblioteca deste modo na MainWindow
        mode = self.parent.mode
        library = self.parent.game_library

        # Número de items por fileira na grid
        items_per_row = 7  

        # Itera sob o dicionário da biblioteca
        for idx, item in enumerate(library):
            # Extrai o dicionário e o campo de data do dicionário
            item_dict = library[item]
            data = item_dict['data']

            # Cria o objeto para exibir este item na biblioteca
            item_displayer = LibraryItemDisplayer(self.library_content, mode, data=data)
            # Configura os elementos do slot da grid de acordo com os dados do item da biblioteca
            image_path = os.path.join(path_to_folder, f'caching/images_cache/{mode}/{item}.png')
            item_displayer.image_thumb.setPixmap(QPixmap(image_path))
            item_displayer.title.setText(item)
            item_displayer.rating_bar.setText(item_dict['rating'])
            item_displayer.status_bar.setText(item_dict['state'])

            # Conecta o botão de remoção do item
            item_displayer.removal_button.clicked.connect(lambda _, name=item: self.remove_item(name))

            # Adiciona os items a grid de modo que haja 7 items por fileira
            rows = idx // items_per_row
            collums = idx % items_per_row
            self.libary_grid.addWidget(item_displayer, rows, collums)

        # Adiciona um item expansível ao final de cada linha para alinhar os itens à esquerda
        for row in range((len(library) + items_per_row - 1) // items_per_row):
            spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.libary_grid.addItem(spacer, row, items_per_row)

        # Preenche a grid da biblioteca com itemdisplayers invisíveis de forma que haja pelo menos 3 fileiras para melhor formatação
        for _ in range(3):
            for _ in range(items_per_row):
                item_displayer = LibraryItemDisplayer(self.library_content, mode)
                item_displayer.make_invisible()
                self.libary_grid.addWidget(item_displayer)

    def remove_item(self, item):
        library = self.parent.game_library
        if item in library:
            del library[item]
            self.update()

# Classe para mostrar um item na biblioteca com sua imagem, nome, rating e status
class LibraryItemDisplayer(QWidget):
    def __init__(self, parent, mode, data=None):
        super().__init__(parent)
        self.setFixedSize(166, 280)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Imagem
        self.image_thumb = QLabel(self)
        self.image_thumb.setAlignment(Qt.AlignCenter)
        self.image_thumb.setScaledContents(True)

        # Botão para remover item
        self.removal_button = QPushButton(self.image_thumb)
        self.removal_button.setIcon(QIcon(os.path.join(path_to_folder, 'assets/remove_button.png')))
        self.removal_button.setStyleSheet("background-color: transparent; border: none;")
        self.removal_button.move(139, 162)

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
        self.removal_button.hide()
        self.title.setStyleSheet("background-color: transparent; border: none;")
        self.rating_bar.setStyleSheet("background-color: transparent; border: none;")
        self.status_bar.setStyleSheet("background-color: transparent; border: none;")