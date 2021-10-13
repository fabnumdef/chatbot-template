import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, UserUttered

proba_score = 0.5

def ask_question_to_piaf(self,
                         dispatcher: CollectingDispatcher,
                         tracker: Tracker,
                         domain: Dict[Text, Any],
                         question: str):
    # update question string
    question = question.strip()
    last_char = question[-1]
    if last_char != '?':
        question = question + ' ?'

    theme = tracker.get_slot('theme')
    sub_theme = tracker.get_slot('sub_theme')
    directory = tracker.get_slot('directory')
    questions_answered = tracker.get_slot('questions_answered')
    url = "https://piaf.datascience.etalab.studio/dila/query"
    data = {"query": f"{question}", "top_k_reader": 3, "top_k_retriever": 5}

    if theme and not sub_theme and not directory:
        data['filters']['theme'] = theme
    elif sub_theme and not directory:
        data['filters']['sous_theme'] = sub_theme
    elif directory:
        data['filters']['dossier'] = directory

    print('asking piaf', question, data['filters'])

    global response
    response = requests.post(url, json=data).json()

    if not response['results'][0]['answers']:
        response = None
    else:
        for r in response['results'][0]['answers']:
            n = r.get('meta').get('name')
            if n not in questions_answered:
                response = r
                questions_answered = questions_answered + [n]
                break

    print(response)

    if response is not None:
        answer = response.get('answer')
        probability = response.get('probability')
        score = response.get('score')
        context = response.get('context')
        link = response.get('meta').get('link')
        name = response.get('meta').get('name')

        if probability >= proba_score:
            # if score is not None and score >= proba_score:
            dispatcher.utter_message(f"J'ai trouvé la réponse suivante : \n {answer}")

            dispatcher.utter_message(f"Dans le corps de texte suivant : {context}")
            dispatcher.utter_message(template = "utter_send_card", payload = link, title = 'Voir la fiche')
    else:
        probability = 0

    # PIAF 1
    if not tracker.get_slot('ask_piaf_1') or not tracker.get_slot('ask_piaf_1_ok'):
        if probability >= proba_score:
            return [SlotSet('ask_piaf_1', True), SlotSet('ask_piaf_1_ok', True), SlotSet('question', question), SlotSet('questions_answered', questions_answered)]
        elif probability < proba_score and not sub_theme:
            print('not sub theme')
            return [SlotSet('ask_piaf_1', True), SlotSet('question', question)]
        elif probability < proba_score and not directory:
            print('not directory')
            return [SlotSet('ask_piaf_1', True), SlotSet('question', question)]
        elif probability < proba_score and directory:
            print('directory')
            return [SlotSet('ask_piaf_1', True), SlotSet('question', question)]
    # PIAF 2
    else:
        if probability >= proba_score:
            return [SlotSet('ask_piaf_2', True), SlotSet('ask_piaf_2_ok', True), SlotSet('question', question), SlotSet('questions_answered', questions_answered)]
        else:
            return [SlotSet('ask_piaf_2', True), SlotSet('question', question)]

    return []
