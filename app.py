from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)



def lancer():
    stream = open("AddToBDD.py")
    lu = stream.read()
    exec(lu)


@app.route('/')
def index():
    conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
    conn.text_factory = str
    cur = conn.cursor()
    print("Connexion reussie à SQLite")
    cur.execute("SELECT * FROM Etudiant")
    posts=cur.fetchall()
    cur.close()
    conn.close()
    print("Connexion SQLite est fermee")
    return render_template('pageBDD.html',posts=posts)


@app.route('/ajouter/')
def pageAjouter():
    return render_template('ajouter.html')

@app.route('/index/', methods=['POST'])
def ajouterEtRetour():
    lancer()
    conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
    conn.text_factory = str
    cur = conn.cursor()
    print("Connexion reussie à SQLite")
    cur.execute("SELECT * FROM Etudiant")
    posts=cur.fetchall()
    cur.close()
    conn.close()
    print("Connexion SQLite est fermee")
    return render_template('/pageBDD.html',posts=posts)