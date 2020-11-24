import json

with open('data/tree.json') as json_file:
    data = json.load(json_file)['data']

def return_themes():
    print('return themes')
    buttons = []
    for theme in data:
        if theme['id'] is None:
            id = 'null'
        else:
            id = theme['id']
        buttons.append({'payload': '/choose_theme{"theme":"' + id + '"}', 'title': theme['name']})
    return buttons

def return_sub_themes(theme_id: str):
    print('return sub themes from theme : ', theme_id)
    theme = next((x for x in data if x['id'] == theme_id), None)
    buttons = []
    for sub_theme in theme['data']:
        if sub_theme['name'] is None:
            id = 'null'
        else:
            id = sub_theme['name']
        buttons.append(
            {'payload': '/choose_sub_theme{"sub_theme":"' + id + '"}', 'title': sub_theme['name']})
    return buttons

def return_directories(theme_id: str, sub_theme_id: str):
    print('return directories from theme : ', theme_id, sub_theme_id)
    theme = next((x for x in data if x['id'] == theme_id), None)
    sub_theme = next((x for x in theme['data'] if x['name'] == sub_theme_id), None)
    buttons = []
    for directory in sub_theme['data']:
        if directory['id'] is None:
            id = 'null'
        else:
            id = directory['id']
        buttons.append(
            {'payload': '/choose_directory{"directory":"' + id + '"}', 'title': directory['name']})
    return buttons

def return_sub_directories(theme_id: str, sub_theme_id: str, directory_id: str):
    print('return sub directories from theme : ', theme_id, sub_theme_id, directory_id)
    theme = next((x for x in data if x['id'] == theme_id), None)
    sub_theme = next((x for x in theme['data'] if x['name'] == sub_theme_id), None)
    directory = next((x for x in sub_theme['data'] if x['id'] == directory_id), None)
    buttons = []
    for sub_directory in directory['data']:
        if sub_directory['name'] is None:
            id = 'null'
        else:
            id = sub_directory['name']
        buttons.append(
            {'payload': '/choose_sub_directory{"sub_directory":"' + id + '"}', 'title': sub_directory['name']})
    return buttons

def return_cards(theme_id: str, sub_theme_id: str, directory_id: str, sub_directory_id: str):
    print('return cards from theme : ', theme_id, sub_theme_id, directory_id, sub_directory_id)
    theme = next((x for x in data if x['id'] == theme_id), None)
    sub_theme = next((x for x in theme['data'] if x['name'] == sub_theme_id), None)
    directory = next((x for x in sub_theme['data'] if x['id'] == directory_id), None)
    sub_directory = next((x for x in directory['data'] if x['name'] == sub_directory_id), None)
    buttons = []
    for card in sub_directory['data']:
        if card['id'] is None:
            id = 'null'
        else:
            id = card['id']
        buttons.append({'payload': 'https://www.service-public.fr/particuliers/vosdroits/' + id, 'title': card['name']})
    return buttons
