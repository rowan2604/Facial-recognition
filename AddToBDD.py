from flask import Flask, render_template, request
import mysql.connector

def insertBlob():
    try:
        nom = request.form['nom']
        prenom = request.form['prenom']
        promo = request.form['promo']
        photo1 = "./images/" + request.form['photo1']
        photo2 = "./images/" + request.form['photo2']
        photo3 = "./images/" + request.form['photo3']
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        cur.execute("CREATE TABLE IF NOT EXISTS Etudiant (Nom VARCHAR(100) NOT NULL, Prenom VARCHAR(100) NOT NULL, Promo VARCHAR(100) NOT NULL, Etat INT NOT NULL, Photo1 BLOB NOT NULL, Photo2 BLOB NOT NULL, Photo3 BLOB NOT NULL)")
        sql = "INSERT INTO Etudiant (Nom, Prenom, Promo, Etat, Photo1, Photo2, Photo3) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        with open(photo1, 'rb') as myfile:
            blobFile1= myfile.read()

        with open(photo2, 'rb') as myfile:
            blobFile2= myfile.read()

        with open(photo3, 'rb') as myfile:
            blobFile3= myfile.read()
        
        value = (nom, prenom, promo, 0, blobFile1, blobFile2, blobFile3)
        cur.execute(sql, value)
        conn.commit()
        print("Fichier insere avec succes")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermee")

    except mysql.connector.Error as error:
        print("Erreur lors de l'insertion", error)

insertBlob()