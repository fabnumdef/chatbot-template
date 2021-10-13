import requests

def ask_question_to_piaf(question):
    # update question string
    question = question.strip()
    last_char = sample_str[-1]
    if last_char == '?':
        question = question + ' ?'

    print('asking piaf', question)
    url = "https://piaf.datascience.etalab.studio/dila/query"
    data = {"query": f"{question}", "top_k_reader": 3, "top_k_retriever": 5}
    response = requests.post(url, json=data).json()
    # text = response['answer']
    # proba = response['probability']
    # context = response['context']
    if not response['results'][0]['answers']:
        return None
    else:
        return response['results'][0]['answers'][0]

if __name__ == '__main__':
    response = ask_question_to_piaf("comment faire une carte d'identité ?")
    print(response['answer'])
