# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk.events import AllSlotsReset

from rasa_sdk.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.use_piaf_api import ask_question_to_piaf
from actions.tree import return_themes, return_sub_themes, return_directories, return_sub_directories, return_cards

class ActionAskPiaf(Action):
    def name(self):
        return "action_ask_piaf"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        question = (tracker.latest_message)['text']
        return ask_question_to_piaf(self, dispatcher, tracker, domain, question)

class ActionSendThemes(Action):
    def name(self):
        return "action_send_themes"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        themes = return_themes()
        dispatcher.utter_message(f"Sélectionnez le sujet de votre demande :")
        dispatcher.utter_message(buttons = themes)
        return []

class ActionSendSubThemes(Action):
    def name(self):
        return "action_send_sub_themes"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        theme = tracker.get_slot('theme')
        sub_themes = return_sub_themes(theme)
        dispatcher.utter_message(f"Votre question concerne :")
        dispatcher.utter_message(buttons = sub_themes)
        return []

class ActionSendDirectories(Action):
    def name(self):
        return "action_send_directories"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        theme = tracker.get_slot('theme')
        sub_theme = tracker.get_slot('sub_theme')
        directories = return_directories(theme, sub_theme)
        dispatcher.utter_message(f"Choisissez parmis les thèmes suivants :")
        dispatcher.utter_message(buttons = directories)
        return []

class ActionSendSubDirectories(Action):
    def name(self):
        return "action_send_sub_directories"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        theme = tracker.get_slot('theme')
        sub_theme = tracker.get_slot('sub_theme')
        directory = tracker.get_slot('directory')
        sub_directories = return_sub_directories(theme, sub_theme, directory)
        dispatcher.utter_message(f"Choisissez parmis les thèmes suivants :")
        dispatcher.utter_message(buttons = sub_directories)
        return []

class ActionSendCards(Action):
    def name(self):
        return "action_send_cards"

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
        cards = return_cards(theme, sub_theme, directory, sub_directory)
        dispatcher.utter_message(f"Choisissez parmis les fiches suivantes :")
        dispatcher.utter_message(buttons = cards)
        return []
