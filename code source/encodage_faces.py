from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

print("SCRIPT ENCODAGE_FACES LAUNCH")

argument_ligne_commande= argparse.ArgumentParser()
argument_ligne_commande.add_argument("--i",'--set_image_recognition',required=True,help="Chemin d'accees aux images de reconnaissance")
#les arguments de ligne de commande sont la pour spécifier le chemin de l'image d'entrée.
argument_ligne_commande.add_argument("--d","--detection-method",type=str,default="hog",help="Methode de detection d'image")
#Avant de pouvoir encoder des visages dans des images, nous devons d'abord les détecter .
argument_ligne_commande.add_argument("-e", "--encodings", required=True,help="path to serialized db of facial encodings")
args=vars((argument_ligne_commande.parse_args()))

# récupérer les chemins vers les images d'entrée dans notre ensemble de données
print ( "[INFO] Création d'une liste de tous les chemins des images" )
imagePaths=list(paths.list_images(args["i"]))

#initialiser deux listes avant notre traitement : Encodages_visage_connu et nom_connu, respectivement. 
#Ces deux listes contiendront les encodages de visage et les noms correspondants pour chaque personne de l'ensemble de données

Encodages_visage_connu=[]
nom_connu=[]
count_picture=len(imagePaths)
#Parcours de toute les images qu'on a dans face
#Nous bouclons sur les chemins de chacune des images.
for(i,imagePaths) in enumerate(imagePaths):
    #nous allons extraire le Nom de la personne du imagePath
    #print(imagePaths)# ce qui donne comme résultat faces\nom.extension
    print("[INFO] Traitement d'image {}/{}".format(i+1,count_picture))
    nom=imagePaths.split(os.path.sep)[-2]
    #nom=nom.split(".")
    #nom=nom[0]
    print(nom)
    # charger l'image d'entrée et la convertir à partir de BGR (commande OpenCV)
	# à l'ordre dlib (RVB)
    image=cv2.imread(imagePaths)
    rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#Localisation des images + calcul des encodages à l'aide de la méthode cnn
    boxes=face_recognition.face_locations(rgb,model=args["d"])
    encodings = face_recognition.face_encodings(rgb, boxes) #transforme les têtes en un vecteur de 128 nombre partie encodage
    for encoding in encodings:
        Encodages_visage_connu.append(encoding)
        nom_connu.append(nom)

print("[INFO] serializing encodings...")
data = {"encodings": Encodages_visage_connu, "names": nom_connu}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data)) #fichier qui contient le vecteur de 128 nombres de chaque visage qui caracterise un visage et permet de l'identifier
f.close()
#Maintenant étant donnée que nous avons ce fichier il suffit de reconnaitre les visages

#Explication de ce qu'est un fichier pickle
#https://www.quennec.fr/trucs-astuces/langages/python/python-le-module-pickle






