import sqlite3

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

insertBlob("CRESPEL", "Rémy", "CIR3", 1,  "C:\Rémy\CIR3\Projet fin d'année\Geass.jpg")