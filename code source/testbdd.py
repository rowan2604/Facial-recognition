import mysql.connector

conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com",
                               user="b8523d276180fb", password="e548c5fe", 
                               database="heroku_432d5a7d6f44b44")

try:
    cursor = conn.cursor()
    print("CONNEXION BDD SUCCEED")
    photo="faces/mbappee.jpg"
    #with open(photo, 'rb') as myfile:
        #blobFile= myfile.read()
    #etudiant = ("Kaddouri", "Abderzak","CIR3", 0,blobFile)
    #cursor.execute("""INSERT INTO etudiant (Nom, Prenom,Promo,Etat,Photo) VALUES( %s, %s, %s,%s,%s)""", etudiant)

    sql = "SELECT Prenom,Photo FROM etudiant WHERE id=15"
    cursor.execute(sql)
    resultat=cursor.fetchall() 
    conn.commit()
except (Exception):
    print("ERROR")
