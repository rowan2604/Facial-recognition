import face_recognition
import argparse
import pickle
import cv2
import numpy as numpy

argument_ligne_commande=argparse.ArgumentParser()

argument_ligne_commande.add_argument("-e", "--encodings", required=True,help="path to serialized db of facial encodings")
argument_ligne_commande.add_argument("-i", "--image_analyse", required=True,help="chemin accès de l'image")
argument_ligne_commande.add_argument("-d", "--detection-method", type=str, default="hog",help="Methode de detection d'image cnn(plus lente mais plus precise) ou hog(plus rapide mais moins précise")
args = vars(argument_ligne_commande.parse_args())

# Chargement des têtes connues
print("[INFO] Chargement de l'encodage...")
data = pickle.loads(open(args["encodings"], "rb").read())  #Charge les têtes encodées et les noms connus


# Chargement de l'image d'entrée à analyser and conversion du BGR au RGB
image = cv2.imread(args["image_analyse"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


print("[INFO] Reconnaissance tête...")
boxes = face_recognition.face_locations(rgb,model=args["detection_method"])
encodings = face_recognition.face_encodings(rgb, boxes) #détection de tous les visages dans l'image d'entrée et calcul leur 128-d encodages.
# Initialisation de la liste de nom qui ont été reconnu
noms = []


for encoding in encodings:
	matches = face_recognition.compare_faces(data["encodings"],encoding) #essaye de faire correspondre chaque visage dans l'image d'entrée  à notre ensemble de données de codage connu 
    #A commenter
	if True in matches:
		matchedIdxs = [i for (i, b) in enumerate(matches) if b]
		counts = {}
	
		for i in matchedIdxs:
			name = data["names"][i]
			counts[name] = counts.get(name, 0) + 1
		name = max(counts, key=counts.get)
	else:
		name="unknown"
	noms.append(name)
	for((top,right,bottom,left),name)in zip(boxes,noms):
		cv2.rectangle(image,(left,top),(right,bottom),(0,255,0),2)
		y=top-15 if top -15 > 15 else top + 15
		cv2.putText(image,name,(left,y),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),2)
	

cv2.imshow("Image",image)
cv2.waitKey(0)
	
