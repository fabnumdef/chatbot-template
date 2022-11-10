import json

# TODO
# Changer l'id next des 50#redirect avec 75a6be2a-1e1c-45ea-aa7b-795bd1e811e8
# Mettre le menu principal dans cet ordre:
#"49af38d2-b0ea-4d65-ab18-d56cbb5356fa",
#"13888dd6-de13-43e6-9619-cf42a54a867a",
#"ae8e61a1-fcc1-4db0-ab7e-fcd37cb2dc16",
#"a402454e-1c83-4d16-95d1-1d9a2eaf139c",
#"3a4cc61c-8e78-42cb-899a-3f0df9be49dd",
#"b5a86b01-92c4-4b8e-a0b6-712122d9f776"

# Rajouter next dans le sous menu 1.1 et 5.1

with open('data/tree.json') as json_file:
    data = json.load(json_file)
    excluded_ids = [x for x in data if 'title' in x and ('redirect' in x['title'] or 'menu' in x['title'])]
    excluded_ids = [x['id'] for x in excluded_ids]

def return_tree(item_id, tree_id_selected: list):
    print(item_id, tree_id_selected)
    messages = []
    if not item_id:
        item_id = "41022967-073c-4af5-be10-81c8e617189f"
    item = next((x for x in data if x['id'] == item_id), None)
    while True:
        if 'name' in item and item['name']:
            messages.append(generate_message(item, tree_id_selected))

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