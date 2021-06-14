from __future__ import print_function
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

argument_ligne_commande.add_argument("-e", "--encodings", required=True,help="path to serialized db of facial encodings")
argument_ligne_commande.add_argument("-y", "--display",type=int, default=1,help="afficher ou non l'image de sortie à l'écran")
argument_ligne_commande.add_argument("-d", "--detection-method", type=str, default="hog",help="Methode de detection d'image cnn(plus lente mais plus precise) ou hog(plus rapide mais moins précise")
args = vars(argument_ligne_commande.parse_args())

# Chargement des têtes connues
print("[INFO] Chargement de l'encodage...")
data = pickle.loads(open(args["encodings"], "rb").read())  #Charge les têtes encodées et les noms connus

print("[INFO] starting video stream...")
#flux_video=VideoStream(src=0).start()
flux_video=WebcamVideoStream(src=0).start()
fps = FPS().start()

#time.sleep(1.0) #Permet de laisser le temps à la caméra de s'allumer

conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com",
                               user="bc534e43745e55", password="3db62771", 
                               database="heroku_642c138889636e7")
cursor = conn.cursor()
print("[INFO] CONNEXION BDD SUCCEED")

while True:
    frame=flux_video.read() # renvoie un boolean si le flux est bien lu
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #convertie la video de BGR en RGB
    rgb=imutils.resize(frame,height=240,width=320) #redimensionne la fenêtre avec une largueur de 320
    r=frame.shape [1] / float(rgb.shape [1]) # .shape  renvoie la taille de la frame.
    boxes=face_recognition.face_locations(rgb,model=args["detection_method"]) #détecte la délimitation du visage
    encodings=face_recognition.face_encodings(rgb,boxes) # encode pour chaque visage detecter
    names=[] #initialisation tableau de nom qu'on a detecter
    for encoding in encodings:
        matches=face_recognition.compare_faces(data["encodings"],encoding)
        if True in matches:
            matchedIdxs=[i for(i,b)in enumerate(matches) if b]
            counts={}
            for i in matchedIdxs:
                name=data["names"][i]
                counts[name]=counts.get(name,0)+1
            name=max(counts,key=counts.get)
        else:
            name="Unknown"
        names.append(name)
        print(name)
        for((top,right,bottom,left),name) in zip(boxes,names):
            top=int(top*r)
            right=int(right*r)
            bottom=int(bottom*r)
            left=int(left*r)
            if(name!="Unknown"):
                cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom),(0, 0, 255), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 0, 255), 2)
        if args["display"]>0:
            nom=name.split(" ")
            print(nom[0])
            cursor.execute('UPDATE Etudiant SET Presence=1 WHERE Nom LIKE \'%' + nom[0] + '%\' AND Presence=$')
            #cursor.execute('UPDATE Etudiant SET Presence=0 WHERE Nom LIKE \'%' + nom[0] + '%\' AND Presence=%') #Mettre sur un autre pc
            conn.commit()
            cv2.imshow("Frame",frame)
    fps.update()
    key=cv2.waitKey(1) & 0xFF
    if key ==ord("q"):
        break
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows
flux_video.release()
cursor.close()
conn.close()
print("[INFO] MySQL connection is closed")

        
        
        

        	
	    






