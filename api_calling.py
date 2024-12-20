import requests, os
from app_function_data import path_to_folder

# API Keys
GIANT_BOMB_API = "7c3d6fc91c3c089a173e05efa8c28ecda8a79a40" # Games database

# Função para pesquisar nomes de jogos no GiantBomb 
def get_game_data(game_name, API_KEY=GIANT_BOMB_API):
    """
    param game_name (string): Nome do jogo a ser pesquisado
    return games (list): Lista de resultados de pesquisa, cada resultado é um dicionário de informações sobre um jogo com as seguintes keys:
    ['aliases', 'api_detail_url', 'date_added', 'date_last_updated', 'deck', 'description', 'guid', 'id', 'image', 'image_tags', 'name', 'site_detail_url', 'resource_type']
    image é também um dicionário com as keys: ['icon_url', 'medium_url', 'screen_url', 'screen_large_url', 'small_url', 'super_url', 'thumb_url', 'tiny_url', 'original_url', 'image_tags']
    """

    url = f'https://www.giantbomb.com/api/search/?api_key={API_KEY}&format=JSON&query={game_name}'
    response = requests.get(url, headers={'user-agent':'newcoder'})
    if response.status_code == 200:
        search_results = response.json().get("results", [])
        games = [game for game in search_results if game.get('resource_type') == 'game']
        return games
    else:
        return []

def url_to_png(mode, data, file_name):
    """
    param mode (string): modo do app ou game
    param data (dict): 1 resultado de uma pesquisa em uma das APIs
    param file_name: nome que o png deve ter
    Função para salvar imagens no cache e evitar requests repetidas da mesma imagem
    """
    if mode == 'game':
        url = f'{data.get('image', {}).get('original_url')}'
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            path = os.path.join(path_to_folder, f'caching/images_cache/{mode}/{file_name}.png')
            with open(path, 'wb') as file:
                file.write(response.content)
        except Exception as e:
            print(e)
