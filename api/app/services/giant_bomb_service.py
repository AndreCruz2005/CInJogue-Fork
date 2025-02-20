import requests
import os
from dotenv import load_dotenv


load_dotenv()
GIANT_BOMB_API_KEY = os.getenv('GIANT_BOMB_API_KEY')

def search_game_on_giant_bomb(game_name):
    """
    Pesquisa por jogos na API do Giant Bomb com base no nome do jogo fornecido.

    Args:
        game_name (str): Nome do jogo a ser pesquisado.

    Returns:
        list: Lista de dicionários contendo informações dos jogos encontrados.
    """
    url = 'https://www.giantbomb.com/api/search/'
    params = {
        'api_key': GIANT_BOMB_API_KEY,
        'format': 'json',
        'query': game_name,
        'resources': 'game'
    }
    headers = {'User-Agent': 'GameLibraryAPI'}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])
    else:
        return []
