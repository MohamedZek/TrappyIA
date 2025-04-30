from flask import Flask, render_template, request
import json
import spacy
from fuzzywuzzy import fuzz
from unidecode import unidecode

app = Flask(__name__)

with open ('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

nlp = spacy.load("fr_core_news_sm")

processed_symptomes = {unidecode(k.lower()): k for k in data}

def trouver_symptomes(user_input):
    doc = nlp(user_input)
    tokens = [unidecode(token.lemma_.lower()) for token in doc if not token.is_stop and not token.is_punct]

    matches = []

    for token in tokens:
        best_score = 0
        best_symptome = None
        for symptome_clean, symptome_original in processed_symptomes.items():
            score = fuzz.partial_ratio(token, symptome_clean)
            if score > best_score and score > 70:  # seuil à ajuster
                best_score = score
                best_symptome = symptome_original
        if best_symptome and best_symptome not in matches:
            matches.append(best_symptome)

    return matches

    
@app.route('/')
def index():
    return render_template('index.html', user_input=None, response=None)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input'].lower()
    input_clean = unidecode(user_input)

    symptomes_detectes = trouver_symptomes(input_clean)

    if not symptomes_detectes:
        response = "Pouvez-vous préciser s'il vous plaît, j'ai du mal à détecter votre symptôme."
    else:
        response = ""
        for symptome in symptomes_detectes:
            infos = data[symptome]
            conseil = infos["conseil"]
            specialiste = infos["medecin"]
            response += (f"Voici les symptômes que vous avez cités : {symptome}.\n"
                         f"{conseil}\n"
                         f"Veuillez consulter un {specialiste}\n"
                         f"Ceci ne remplace une vraie consultation médicale.\n\n")

    return render_template('index.html', user_input=user_input, response=response.strip())


