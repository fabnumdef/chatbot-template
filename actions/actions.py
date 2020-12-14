# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk.events import SlotSet

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.tree import return_tree, return_full_tree

class ActionSendTree(Action):
    def name(self):
        return "action_send_tree"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        messages = return_tree(tracker.get_slot('tree_id'), tracker.get_slot('tree_id_selected'))

        if tracker.get_slot('tree_id'):
            tree_id_selected = tracker.get_slot('tree_id_selected') + [tracker.get_slot('tree_id')]
        else:
            tree_id_selected = tracker.get_slot('tree_id_selected')

        for message in messages:
            print (message)
            if 'buttons' in message:
                dispatcher.utter_message(text = message['text'], buttons = message['buttons'])
            else:
                dispatcher.utter_message(text = message['text'])
        return [SlotSet(key = "tree_id_selected", value = tree_id_selected)]

class ActionSendFullTree(Action):
    def name(self):
        return "action_send_full_tree"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        data = return_full_tree(None, [], [])
        dispatcher.utter_message(json_message  = {'data': {'custom': {'conversation': data}}})
        return []
