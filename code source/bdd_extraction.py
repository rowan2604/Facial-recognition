import mysql.connector
import os
import shutil



print("SCRIPT BDD_EXTRACTION LAUNCH")

conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com",
                               user="b8523d276180fb", password="e548c5fe", 
                               database="heroku_432d5a7d6f44b44")



try:
    cursor = conn.cursor()
    print("CONNEXION BDD SUCCEED")

    #Insertion d'une photo
    #photo="faces/mbappee.jpg"
    #with open(photo, 'rb') as myfile:
        #blobFile= myfile.read()
    #etudiant = ("Kaddouri", "Abderzak","CIR3", 0,blobFile)
    #cursor.execute("""INSERT INTO etudiant (Nom, Prenom,Promo,Etat,Photo) VALUES( %s, %s, %s,%s,%s)""", etudiant)
    #Fin Insertion

    sql = """SELECT * FROM etudiant"""
    cursor.execute(sql)
    resultat=cursor.fetchall()
    
    for info in resultat:
        if os.path.exists("bdd_picture/"+info[2]+info[1]):
            print("je suis la")
            shutil.rmtree("bdd_picture/"+info[2]+info[1])
            print("je suis la")
        os.mkdir("bdd_picture/"+info[2]+info[1])
        image=info[5]
        path="C:/Users/Abderzak/Desktop/Ecole ISEN/CIR3/Projet Reconnaissance faciale code/code source/bdd_picture/"+info[2]+info[1]+"/"+info[2]+" "+info[1]+".jpeg"
        with open(path, 'wb') as myfile:
            myfile.write(image)
   

    conn.commit()

except (Exception) as error:
    print("Error",error)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")
