# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk.events import AllSlotsReset, SlotSet

from rasa_sdk.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.use_piaf_api import ask_question_to_piaf
from actions.tree import return_tree

class ActionAskPiaf(Action):
    def name(self):
        return "action_ask_piaf"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.latest_message['intent']['confidence'] < 0.9:
            question = tracker.latest_message['text']
        else:
            question = tracker.get_slot('question')

        return ask_question_to_piaf(self, dispatcher, tracker, domain, question)

class ActionSendTree(Action):
    def name(self):
        return "action_send_tree"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        theme = tracker.get_slot('theme')
        sub_theme = tracker.get_slot('sub_theme')
        directory = tracker.get_slot('directory')
        sub_directory = tracker.get_slot('sub_directory')
        [text, items, is_cards] = return_tree(theme, sub_theme, directory, sub_directory)
        dispatcher.utter_message(text = text, buttons = items)
        if is_cards:
            return [SlotSet('send_cards', True)]
        else:
            return []