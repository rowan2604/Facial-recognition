import mysql.connector
import os
import shutil



print("SCRIPT BDD_EXTRACTION LANCEMENT")

#Connexion à la bdd
conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com",
                               user="bc534e43745e55", password="3db62771", 
                               database="heroku_642c138889636e7")



try:
    cursor = conn.cursor()
    print("CONNEXION BDD SUCCEED")
    sql = """SELECT * FROM etudiant"""
    cursor.execute(sql)
    resultat=cursor.fetchall()

    #Permet de supprimer tous les dossiers de bdd_picture
    file=os.listdir('bdd_picture/')

    for i in range (len(file)):
        shutil.rmtree("bdd_picture"+"/"+file[i])    
    
    for info in resultat:
        os.mkdir("bdd_picture/"+info[1]+" "+info[2]) #permet de creer des dossiers au noms des personnes présentent en bdd
        image1=info[5] # recupération des images en bdd
        image2=info[6]
        image3=info[7]
        image4=info[8]
        image5=info[9]
        image6=info[10]
        image7=info[11]
        path1="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"1"+".jpeg" #insertion des images dans les bon path
        path2="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"2"+".jpeg"
        path3="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"3"+".jpeg"
        path4="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"4"+".jpeg"
        path5="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"5"+".jpeg"
        path6="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"6"+".jpeg"
        path7="bdd_picture/"+info[1]+" "+info[2]+"/"+info[1]+" "+info[2]+"7"+".jpeg"
        with open(path1, 'wb') as myfile:
            myfile.write(image1) # conversion de blob à image
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
        conn.close() # deconnexion de la bdd
        print("MySQL connection is closed")
