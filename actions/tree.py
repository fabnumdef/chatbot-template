import json

with open('data/tree.json') as json_file:
    data = json.load(json_file)

def return_tree(theme_id: str = None, sub_theme_id: str = None, directory_id: str = None, sub_directory_id: str = None):
    print('return item from tree : ', theme_id, sub_theme_id, directory_id, sub_directory_id)
    parent_item = data
    search_attribute = 'name'
    if theme_id:
        parent_item = next((x for x in parent_item['data'] if x['name'] == theme_id), None)
        # search_attribute = 'name'

    if sub_theme_id:
        parent_item = next((x for x in parent_item['data'] if x['name'] == sub_theme_id), None)
        # search_attribute = 'id'

    if directory_id:
        parent_item = next((x for x in parent_item['data'] if x['name'] == directory_id), None)
        # search_attribute = 'name'

    if sub_directory_id:
        parent_item = next((x for x in parent_item['data'] if x['name'] == sub_directory_id), None)
        # search_attribute = 'id'

    buttons = []
    text = ''
    is_cards = False
    for item in parent_item['data']:
        if item[search_attribute] is None:
            id = 'null'
        else:
            id = item[search_attribute]

        if item['type'] == 'fiche':
            text = 'Choisissez parmis les fiches suivantes :'
            buttons.append({'payload': 'https://www.service-public.fr/particuliers/vosdroits/' + id, 'title': item['name']})
            is_cards = True
        elif item['type'] == 'theme':
            text = 'Sélectionnez le sujet de votre demande :'
            buttons.append({'payload': '/choose_theme{"theme":"' + id + '"}', 'title': item['name']})
        elif item['type'] == 'sous_theme':
            text = 'Votre question concerne :'
            buttons.append({'payload': '/choose_sub_theme{"sub_theme":"' + id + '"}', 'title': item['name']})
        elif item['type'] == 'dossier':
            text = 'Choisissez parmis les dossiers suivants :'
            buttons.append({'payload': '/choose_directory{"directory":"' + id + '"}', 'title': item['name']})
        elif item['type'] == 'sous_dossier':
            text = 'Choisissez parmis les sous-dossiers suivants :'
            buttons.append({'payload': '/choose_sub_directory{"sub_directory":"' + id + '"}', 'title': item['name']})

    return [text, buttons, is_cards]
