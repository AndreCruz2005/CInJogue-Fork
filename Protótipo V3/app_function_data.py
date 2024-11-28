import os
# Caminho para o diretório onde este arquivo está, este arquivo deve ficar no mesmo diretório que todos os outros que usam essa variável
path_to_folder = os.path.dirname(os.path.abspath(__file__))

app_color_palette = {
    'dark': {'movie':"#280606", 'game':"#070F2B"},
    'dark-medium': {'movie':"#541A1A", 'game':"#1B1A55"},
    'medium': {'movie':"#BE3144", 'game':"#535C91"},
    'light': {'movie':"#F05941", 'game':"#9290C3"}
}

