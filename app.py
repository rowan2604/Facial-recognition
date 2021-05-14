import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def lancer():
    stream = open("AddToBDD.py")
    lu = stream.read()
    exec(lu)


@app.route('/')
def index():
    return render_template('pageBDD.html')

@app.route('/ajouter/')
def pageAjouter():
    return render_template('ajouter.html')

@app.route('/index/', methods=['POST'])
def ajouterEtRetour():
    lancer()
    return render_template('pageBDD.html')