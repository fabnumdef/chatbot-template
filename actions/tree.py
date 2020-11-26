import json

with open('data/tree.json') as json_file:
    data = json.load(json_file)

def return_tree(item_id):
    print(item_id)
    messages = []
    if not item_id:
        item_id = "03240eb5-bc48-4c13-90e0-dcf79b442f08"
    item = next((x for x in data if x['id'] == item_id), None)
    while True:
        print(item)
        if 'choices' in item:
            messages[-1]['buttons'] = generate_message(item)['buttons']
        else:
            messages.append(generate_message(item))
        if 'next' in item and item['next']:
            item = next((x for x in data if x['id'] == item['next']), None)
        else:
            break

    return messages


def generate_message(item):
    message = {}
    if 'choices' in item and item['choices']:
        message['text'] = ''
        message['buttons'] = generate_buttons(item)
    elif item['type'] == 'Text':
        message['text'] = item['name']
    return message

def generate_buttons(item):
    buttons = []
    for choice in item['choices']:
        sub_item = next((x for x in data if x['id'] == choice), None)
        buttons.append({'payload': '/send_tree{"tree_id":"' + sub_item['next'] + '"}', 'title': sub_item['name']})
    return buttons
