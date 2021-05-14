import sqlite3
from flask import Flask, render_template, request

def insertBlob():
    try:
        nom = request.form['nom']
        prenom = request.form['prenom']
        promo = request.form['promo']
        photo = "./images/" + request.form['photo']
        conn = sqlite3.connect('etudiant.db')
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        cur.execute("CREATE TABLE IF NOT EXISTS ETUDIANT (id INTEGER PRIMARY KEY AUTOINCREMENT, Nom TEXT NOT NULL, Prenom TEXT NOT NULL, Promo TEXT NOT NULL, Etat INTEGER NOT NULL, Photo BLOB NOT NULL)")
        sql = "INSERT INTO ETUDIANT (nom, prenom, promo, etat, photo) VALUES (?,?,?,?,?)"

        with open(photo, 'rb') as myfile:
            blobFile= myfile.read()
        
        value = (nom, prenom, promo, 0, blobFile)
        cur.execute(sql, value)
        conn.commit()
        print("Fichier insere avec succes")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermee")

    except sqlite3.Error as error:
        print("Erreur lors de l'insertion", error)

insertBlob()