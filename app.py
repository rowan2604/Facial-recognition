import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def insertBlob(nom, prenom, promo, état, photo):
    try:
        conn = sqlite3.connect('etudiant.db')
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion réussie à SQLite")
        cur.execute("CREATE TABLE ETUDIANT (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL, Prénom TEXT NOT NULL, Promo TEXT NOT NULL, état INTEGER NOT NULL, image BLOB NOT NULL)")
        sql = "INSERT INTO ETUDIANT (nom, prénom, promo, état, image) VALUES (?,?,?,?,?)"

        with open(photo, 'rb') as myfile:
            blobFile= myfile.read()
        
        value = (nom, prenom, promo, état, blobFile)
        cur.execute(sql, value)
        conn.commit()
        print("Fichier inséré avec succès")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")

    except sqlite3.Error as error:
        print("Erreur lors de l'insertion", error)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/test/', methods=['POST'])
def monTest():
    nom = request.form['nom']
    prenom = request.form['prenom']
    promo = request.form['promo']
    photo = "./images/" + request.form['photo']

    try:
        conn = sqlite3.connect('etudiant.db')
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion réussie à SQLite")
        sql = "INSERT INTO ETUDIANT (nom, prénom, promo, état, image) VALUES (?,?,?,?,?)"

        with open(photo, 'rb') as myfile:
            blobFile= myfile.read()
        
        value = (nom, prenom, promo, 1, blobFile)
        cur.execute(sql, value)
        conn.commit()
        print("Fichier inséré avec succès")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")

    except sqlite3.Error as error:
        print("Erreur lors de l'insertion", error)
    
    return render_template('index.html')