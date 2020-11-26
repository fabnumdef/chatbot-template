# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.tree import return_tree

class ActionSendTree(Action):
    def name(self):
        return "action_send_tree"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        messages = return_tree(tracker.get_slot('tree_id'))
        for message in messages:
            print (message)
            if 'buttons' in message:
                dispatcher.utter_message(text = message['text'], buttons = message['buttons'])
            else:
                dispatcher.utter_message(text = message['text'])
        return []
