from flask import Flask, render_template, request
import mysql.connector

def insertBlob():
    try:
        nom = request.form['nom']
        prenom = request.form['prenom']
        promo = request.form['promo']
        photo = "./images/" + request.form['photo']
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        cur.execute("CREATE TABLE IF NOT EXISTS Etudiant (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, Nom VARCHAR(100) NOT NULL, Prenom VARCHAR(100) NOT NULL, Promo VARCHAR(100) NOT NULL, Etat INT NOT NULL, Photo BLOB NOT NULL)")
        sql = "INSERT INTO Etudiant (Nom, Prenom, Promo, Etat, Photo) VALUES (%s,%s,%s,%s,%s)"

        with open(photo, 'rb') as myfile:
            blobFile= myfile.read()
        
        value = (nom, prenom, promo, 0, blobFile)
        cur.execute(sql, value)
        conn.commit()
        print("Fichier insere avec succes")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermee")

    except mysql.connector.Error as error:
        print("Erreur lors de l'insertion", error)

insertBlob()