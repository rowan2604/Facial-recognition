from imutils.video import WebcamVideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import cv2
import time
import mysql.connector

print("SCRIPT RECOGNITION_FACES_VIDEO LAUNCH")

argument_ligne_commande=argparse.ArgumentParser()

argument_ligne_commande.add_argument("-e", "--encodings", required=True,help="Chemin où sont sérialisé les visages (Visage encodé)")
argument_ligne_commande.add_argument("-y", "--display",type=int, default=1,help="afficher ou non l'image de sortie à l'écran")
#permet grâce à cette argument de montrer ou non le flux vidéo
argument_ligne_commande.add_argument("-d", "--detection-method", type=str, default="hog",help="Methode de detection d'image cnn(plus lente mais plus precise) ou hog(plus rapide mais moins précise")
#permet de spécifier la méthode de reconnaissance soit hog => plus rapide mais moins précise ou cnn => plus précise mais moins rapide
args = vars(argument_ligne_commande.parse_args())

# Chargement des têtes connues
print("[INFO] Chargement de l'encodage...")
data = pickle.loads(open(args["encodings"], "rb").read())  #Charge les têtes encodées et les noms connus

print("[INFO] LANCEMENT DE LA CAMERA")
flux_video=WebcamVideoStream(src=0).start() #récupère le flux de la webcam
fps = FPS().start() #lance les FPS pour faire des test de performance

#time.sleep(1.0) #Permet de laisser le temps à la caméra de s'allumer

#Connexion à la BDD
conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com",
                               user="bc534e43745e55", password="3db62771", 
                               database="heroku_642c138889636e7")
cursor = conn.cursor()
print("[INFO] CONNEXION BDD REUSSIE")

while True:
    frame=flux_video.read() # renvoie un boolean si le flux est bien lu
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #convertie la video de BGR en RGB
    rgb=imutils.resize(frame,height=240,width=320) #redimensionne la fenêtre avec une largueur de 320
    r=frame.shape [1] / float(rgb.shape [1]) # .shape  renvoie la taille de la frame.
    boxes=face_recognition.face_locations(rgb,model=args["detection_method"]) #détecte la délimitation du visage
    encodings=face_recognition.face_encodings(rgb,boxes) # encode pour chaque visage detecter
    names=[] #initialisation tableau de nom qu'on a detecter
    #Partie où on compare chaque visage detecté par la caméra par ce qu'on a dans notre fichier encodings.pickle
    for encoding in encodings:
        comparaison=face_recognition.compare_faces(data["encodings"],encoding) #Compare chaque visage détecté par ce qu'on à encodé dans le script encodage_face.py.Cette fonction nous permet de comparer une liste de visage encodé et retourne une liste de True si il y a bien ressemblence.
        if True in comparaison:#nous permet de poser la condition sur la reconnaissance d'une personne qui à l'air d'être dans notre fichier encodings.pickle
            match=[i for(i,b)in enumerate(comparaison) if b] # enumerate donne la valeur et la position de l'élément et le if b nous permet de prendre seulement les élément true de comparaison donc on obtient par exemple [0,2,4,6] correspondant tous un certains nom par exemple l'index 0 correspond au premier nom encodé
            #match est un tableau d'entier composer seulement des index true du tableau comparaison
            compteur={}
            for i in match: # nous permet de boucler sur match et d'assigner à chaque match un nom grâce à son indice
                name=data["names"][i]
                compteur[name]=compteur.get(name,0)+1 # on ajoute 1 à chaque fois que ce nom est présent dans notre liste match
            name=max(compteur,key=compteur.get) # on récupére le nom avec le plus de match et on dit qu'on a reconnu cette personne avec ce nom
        else:
            name="Unknown " # sinon on met nom à inconnu si aucune ressemblence à été detecté
        names.append(name)
        print(name)
        for((top,right,bottom,left),name) in zip(boxes,names): # nous permet de dessiner les carrés autour des visages détecter qu'il soit reconnu ou non
            top=int(top*r)
            right=int(right*r)
            bottom=int(bottom*r)
            left=int(left*r)
            if(name!="Unknown "):# dessine un carré vert si reconnu
                cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
            else:#dessine un carré rouge si inconnu
                cv2.rectangle(frame, (left, top), (right, bottom),(0, 0, 255), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 0, 255), 2)
        if args["display"]>0:
            nom=name.split(" ")
            print(nom[0]+nom[1])
            cursor.execute("UPDATE Etudiant SET Presence='%' WHERE Nom ='" + nom[0] +"'AND Prenom ='"+nom[1]+"'AND Presence='$'") #Permet de changer l'état de l'élève à present si il est absent et reconnu par l'IA
            #cursor.execute("UPDATE Etudiant SET Presence='$' WHERE Nom ='" + nom[0] +"'AND Prenom ='"+nom[1]+"'AND Presence='%'") #Permet de changer l'état de l'élève à present si il est absent et reconnu par l'IA #Mettre sur un autre pc
            conn.commit()
            cv2.imshow("Frame",frame)
    fps.update() #Met a jour le nombre de FPS pour nos test de performance
    key=cv2.waitKey(1) & 0xFF
    if key ==ord("q"):
        break
fps.stop() #arrete le comptage des FPS
print("[INFO] Temps passé: {:.2f}".format(fps.elapsed()))
print("[INFO] Nombre de FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows
flux_video.release()
cursor.close()
conn.close()
print("[INFO] Connexion MYSQL : FERMETURE")

        
        
        

        	
	    






