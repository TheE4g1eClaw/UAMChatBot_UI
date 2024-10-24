from flask import Flask, render_template, request, url_for
import requests
import json
import re
import time
import os

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

nUsuarios = 0

@app.route("/")
def home():
    global nUsuarios
    nUsuarios += 1
    return render_template("index.html", usuarioId = nUsuarios - 1)

@app.route("/ejemplos")
def ejemplos():
    return render_template("ejemplos.html")

@app.route("/get")
def get_bot_response():
    userText = str(request.args.get('msg'))
    id = str(request.args.get('id'))
    data = json.dumps({"sender" : "Rasa" + id,"message" : userText})
    headers = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', data = data, headers = headers)
    response = response.json()
    with open("conversaciones/conversaciones.txt", 'a', encoding='utf-8') as file:
        file.write("Usuario: " + userText + "\n")
        file.write("Chatbot: " + str(response[0]['text']) + "\n")
        file.close()
    return str(response[0]['text'])

        
if __name__ == "__main__":
    app.run(debug = True)
        
    
 