import mysql.connector
import os
import shutil



print("SCRIPT BDD_EXTRACTION LAUNCH")

conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com",
                               user="bc534e43745e55", password="3db62771", 
                               database="heroku_642c138889636e7")



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
        if os.path.exists("bdd_picture/"+info[1]+" "+info[2]):
            shutil.rmtree("bdd_picture/"+info[1]+" "+info[2])
        os.mkdir("bdd_picture/"+info[1]+" "+info[2])
        image1=info[5]
        image2=info[6]
        image3=info[7]
        image4=info[8]
        image5=info[9]
        image6=info[10]
        image7=info[11]
        path1="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"1"+".jpeg"
        path2="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"2"+".jpeg"
        path3="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"3"+".jpeg"
        path4="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"4"+".jpeg"
        path5="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"5"+".jpeg"
        path6="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"6"+".jpeg"
        path7="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"7"+".jpeg"
        with open(path1, 'wb') as myfile:
            myfile.write(image1)
        with open(path2, 'wb') as myfile:
            myfile.write(image2)
        with open(path3, 'wb') as myfile:
            myfile.write(image3)
        with open(path4, 'wb') as myfile:
            myfile.write(image4)
        with open(path5, 'wb') as myfile:
            myfile.write(image5)
        with open(path6, 'wb') as myfile:
            myfile.write(image6)
        with open(path7, 'wb') as myfile:
            myfile.write(image7)

   

    conn.commit()

except (Exception) as error:
    print("Error",error)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")
