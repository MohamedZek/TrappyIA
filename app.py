from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open ('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    
@app.route('/')
def index():
    return render_template('index.html', user_input=None, response=None)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input'].lower()
    response = "Je n'ai pas compris ton symptome."
    
    for symptome, infos in data.items():
        if symptome in user_input :
            conseil = infos["conseil"]
            specialiste = infos["medecin"]
            response = (f"{conseil}\n"
                        f"Tu devrais consulter un {specialiste}\n"
                        f"Cependant, ce conseil ne remplace pas une vraie consultation médicale")
            break
    return render_template('index.html', user_input = user_input, response = response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

# pour Vercel
app = app