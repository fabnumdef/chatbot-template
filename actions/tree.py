import json

# TODO
# Mettre le menu principal dans cet ordre:
# "c43ae085-13e1-48c9-a90e-d85078c0b1c1",
# "690fb2b9-7c75-49ed-ba7e-afc7feacb13a",
# "620c7368-382f-4254-ba2a-cacc83c84db5",
# "0eea0dbc-0f4a-4f47-a094-0540b12a6dce",
# "5699fad2-90a1-4be9-89fe-f22dce13c048",
# "8dafab70-25b2-4c8a-9feb-90f217e7ec9c"

with open('data/tree.json') as json_file:
    data = json.load(json_file)
    excluded_ids = [x for x in data if 'title' in x and ('redirect' in x['title'] or 'menu' in x['title'] or 'Je veux revenir en arrière' in x['name'])]
    excluded_ids = [x['id'] for x in excluded_ids]

def return_tree(item_id, tree_id_selected: list):
    print(item_id, tree_id_selected)
    messages = []
    return_message = {
        "text": "Retour en arrière"
    }
    if not item_id:
        item_id = "41022967-073c-4af5-be10-81c8e617189f"
    item = next((x for x in data if x['id'] == item_id), None)
    while True:
        if 'name' in item and item['name']:
            messages.append(generate_message(item, tree_id_selected))

        if 'choices' in item and not messages:
            messages.append(return_message)

        if 'choices' in item and messages:
            if 'buttons' in messages[-1] and messages[-1]['buttons']:
                messages[-1]['buttons'] = messages[-1]['buttons'] + generate_message(item, tree_id_selected)['buttons']
            else :
                messages[-1]['buttons'] = generate_message(item, tree_id_selected)['buttons']

        if 'next' in item and item['next']:
            item = next((x for x in data if x['id'] == item['next']), None)
        else:
            break

    return messages

def return_full_tree(id, messages, choices_proceeded):
    messages = messages + return_tree(id, [])
    choices_proceeded.append(id)
    for m in reversed(messages):
        if 'buttons' in m and m['buttons']:
            for b in m['buttons']:
                if 'id' in b and b['id'] and b['id'] not in choices_proceeded:
                    messages.append({'text': b['title'], 'from': 'sent'})
                    messages = return_full_tree(b['id'], messages, choices_proceeded)
            m.pop('buttons', None)
    messages[-1]['quick_replies'] = [{'payload': '/send_tree', 'title': 'Relancer le chatbot'}]
    return messages

def generate_message(item, tree_id_selected):
    message = {}
    if 'choices' in item and item['choices']:
        message['text'] = ''
        message['buttons'] = generate_buttons(item, tree_id_selected)

    if item['type'] == 'Text':
        message['text'] = item['name'].replace('<ahref: ', '<a target="_blank" href=')
    return message

def generate_buttons(item, tree_id_selected: list):
    buttons = []
    for choice in item['choices']:
        sub_item = next((x for x in data if x['id'] == choice), None)
        if sub_item['next'] in tree_id_selected and sub_item['id'] not in excluded_ids:
           buttons.append({'payload': None, 'title': sub_item['name']})
        else:
            buttons.append({'payload': '/send_tree{"tree_id":"' + sub_item['next'] + '"}', 'title': sub_item['name'], 'id': sub_item['next']})
    return buttons