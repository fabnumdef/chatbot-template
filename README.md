# Fabrique à chatbots
## Template RASA

L’objectif de la ‘Fabrique à chatbots’ est de détailler les étapes de réalisation d’un chatbot — de l’identification d’un cas d’usage, à la mise en place de l’interface du chatbot — afin de ne pas créer de ruptures dans l’expérience utilisateur, et de fournir les documents/code/template utiles pour la réalisation d’un chatbot.

Ce service est un guide pour la définition d’une problématique de diffusion d’informations se prêtant à une solution « chatbot ».

C’est également une aide pratique pour la constitution d’une base documentaire (template excel) où sont consignées les questions/réponses du chatbot, et pour la réalisation de l’interface qui permet de créer et maintenir le chatbot (back office pour mise à jour de la base documentaire).

### Utilisation

Ce repo est un template de base pour la configuration RASA utilisé par tout chatbot crée via la Fabrique à chatbots.

Pour les informations concernant RASA: [documentation RASA](https://rasa.com/docs/rasa/)

1. Cloner le repo et `cd` dedans
2. `cp endpoints.example.yml endpoints.yml`
3. Editer le fichier `endpoints.yml`
4. Générer les fichiers RASA (`domain.yml`, `data/nlu.json` et `data/stories.md`)
5. `rasa train --augmentation 0`
6. `rasa -dmS rasa run -m models --enable-api --log-file out.log --cors "*" --debug`
