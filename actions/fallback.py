import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, UserUttered
import requests

def return_fallback_suggestions(self,
                         dispatcher: CollectingDispatcher,
                         tracker: Tracker,
                         domain: Dict[Text, Any]):
    banned_intents = ['nlu_fallback', 'phrase_presentation', 'phrase_feedback']
    intents_not_bad = [intent for intent in tracker.latest_message['intent_ranking'] if intent['confidence'] >= 0.2 and intent['name'] not in banned_intents]
    if len(intents_not_bad) <= 0:
        return []

    buttons_to_send = []
    intents_ids = []
    for i in intents_not_bad:
        intents_ids.append(i['name'])

    response = requests.post('http://localhost:3000/api/public/intents', json = intents_ids)
    for i in response.json():
        buttons_to_send.append({"payload": "/" + i['id'], "title": i['mainQuestion']})

    dispatcher.utter_message(text = "J'ai trouvé des propositions qui pourraient correspondre à votre recherche", buttons = buttons_to_send)
