import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from main import MainWindow
from ai_recommendations_region import RecommendedItemDisplayer
from library_region import LibraryItemDisplayer

# pytest -v test_app.py

@pytest.fixture(scope="session")
def app():
    """Cria uma instância do QApplication para a sessão de teste."""
    return QApplication([])

@pytest.fixture
def main_window(app, qtbot):
    """Cria uma instância do MainWindow para cada teste."""
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    return main_window

def test_add_to_library_button(qtbot, main_window):
    print("Iniciando teste: test_add_to_library_button")
    # Simula a adição de um item à biblioteca
    item_displayer = RecommendedItemDisplayer(main_window.ai_recommendation_region.scroll_content, main_window.mode)
    item_displayer.title.setText("Test Game")
    qtbot.mouseClick(item_displayer.add_button, Qt.LeftButton)
    # Verifica se o item foi adicionado à biblioteca
    assert "Test Game" in main_window.game_library
    print("Teste concluído: test_add_to_library_button")

def test_remove_from_library_button(qtbot, main_window):
    print("Iniciando teste: test_remove_from_library_button")
    # Adiciona um item à biblioteca para ser removido
    main_window.game_library["Test Game"] = {'rating': 'unrated', 'state': 'Unplayed', 'data': {}}
    main_window.library_region.update()
    # Encontra o botão de remoção e clica nele
    for item_displayer in main_window.library_region.library_content.children():
        if isinstance(item_displayer, LibraryItemDisplayer) and item_displayer.title.text() == "Test Game":
            qtbot.mouseClick(item_displayer.removal_button, Qt.LeftButton)
            break
    # Verifica se o item foi removido da biblioteca
    assert "Test Game" not in main_window.game_library
    print("Teste concluído: test_remove_from_library_button")

def test_text_input(qtbot, main_window):
    print("Iniciando teste: test_text_input")
    # Simula a entrada de texto no campo de texto
    qtbot.keyClicks(main_window.ai_recommendation_region.user_chat_input, "Recomende um jogo")
    qtbot.keyPress(main_window.ai_recommendation_region.user_chat_input, Qt.Key_Return)
    # Verifica se o texto foi enviado corretamente
    assert main_window.ai_recommendation_region.user_chat_input.text() == ""
    print("Teste concluído: test_text_input")

def test_clear_recommendations_button(qtbot, main_window):
    print("Iniciando teste: test_clear_recommendations_button")
    # Adiciona recomendações para serem limpas
    main_window.game_recommendations['High Priority'] = {'Test Game': {}}
    main_window.ai_recommendation_region.update()
    # Clica no botão de limpar recomendações
    qtbot.mouseClick(main_window.ai_recommendation_region.clear_button, Qt.LeftButton)

    # Verifica se as recomendações foram limpas
    assert not main_window.game_recommendations['High Priority']
    print("Teste concluído: test_clear_recommendations_button")

def test_load_more_recommendations_button(qtbot, main_window):
    print("Iniciando teste: test_load_more_recommendations_button")
    # Adiciona recomendações de baixa prioridade para serem carregadas
    main_window.game_recommendations['Low Priority'] = {'Test Game': {}}
    main_window.ai_recommendation_region.update()
    # Clica no botão de carregar mais recomendações
    qtbot.mouseClick(main_window.ai_recommendation_region.load_button, Qt.LeftButton)
    # Verifica se as recomendações foram movidas para alta prioridade
    assert 'Test Game' in main_window.game_recommendations['High Priority']
    assert 'Test Game' not in main_window.game_recommendations['Low Priority']
    print("Teste concluído: test_load_more_recommendations_button")