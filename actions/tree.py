import json

root_id = "03240eb5-bc48-4c13-90e0-dcf79b442f08"

with open('data/tree.json') as json_file:
    data = json.load(json_file)

def return_tree(item_id, tree_id_selected: list):
    print(item_id, tree_id_selected)
    messages = []
    if not item_id:
        item_id = root_id
    item = next((x for x in data if x['id'] == item_id), None)
    while True:
        print(item)
        if 'choices' in item and messages:
            messages[-1]['buttons'] = generate_message(item, tree_id_selected)['buttons']
        else:
            messages.append(generate_message(item, tree_id_selected))
        if 'next' in item and item['next']:
            item = next((x for x in data if x['id'] == item['next']), None)
        else:
            break

    return messages

def return_full_tree(id = root_id, messages = [], choices_proceeded = []):
    print('return full tree')
    messages = messages + return_tree(id, [])
    choices_proceeded.append(id)
    for m in messages:
        if 'buttons' in m and m['buttons']:
            for b in m['buttons']:
                if 'id' in b and b['id'] and b['id'] not in choices_proceeded:
                    messages.append({'text': b['title'], 'from': 'sent'})
                    messages = return_full_tree(b['id'], messages, choices_proceeded)
            m.pop('buttons', None)
    return messages

def generate_message(item, tree_id_selected):
    message = {}
    if 'choices' in item and item['choices']:
        message['text'] = ''
        message['buttons'] = generate_buttons(item, tree_id_selected)
    elif item['type'] == 'Text':
        message['text'] = item['name']
    return message

def generate_buttons(item, tree_id_selected: list):
    buttons = []
    for choice in item['choices']:
        sub_item = next((x for x in data if x['id'] == choice), None)
        if sub_item['next'] in tree_id_selected:
            buttons.append({'payload': None, 'title': sub_item['name']})
        else:
            buttons.append({'payload': '/send_tree{"tree_id":"' + sub_item['next'] + '"}', 'title': sub_item['name'], 'id': sub_item['next']})
    return buttons