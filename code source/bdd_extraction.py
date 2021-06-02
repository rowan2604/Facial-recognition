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
        if os.path.exists("bdd_picture/"+info[0]+" "+info[1]):
            shutil.rmtree("bdd_picture/"+info[0]+" "+info[1])
        os.mkdir("bdd_picture/"+info[0]+" "+info[1])
        image=info[4]
        image2=info[5]
        image3=info[6]
        path="bdd_picture/"+info[0]+" "+info[1]+"/"+info[0]+" "+info[1]+".jpeg"
        path2="bdd_picture/"+info[0]+" "+info[1]+"/"+info[0]+" "+info[1]+"1"+".jpeg"
        path3="bdd_picture/"+info[0]+" "+info[1]+"/"+info[0]+" "+info[1]+"2"+".jpeg"
        with open(path, 'wb') as myfile:
            myfile.write(image)
        with open(path2, 'wb') as myfile:
            myfile.write(image2)
        with open(path3, 'wb') as myfile:
            myfile.write(image3)

   

    conn.commit()

except (Exception) as error:
    print("Error",error)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")
