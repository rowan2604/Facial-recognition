from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import mysql.connector

ap = argparse.ArgumentParser()

ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-e", "--en", required=True,
	help="path to OpenCV's deep learning face encodings model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.7,
	help="minimum probability to filter weak detections")
ap.add_argument("-a", "--encoding", required=True,
	help="path to model trained to recognize faces")
args = vars(ap.parse_args())

print("[INFO] Chargement des faces_detection_model")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

print("[INFO] Reconnaissance Faciale Debut")

embedder = cv2.dnn.readNetFromTorch(args["en"])
recognizer = pickle.loads(open(args["recognizer"], "rb").read()) #recuperer les nom en label +les visages encodés
le = pickle.loads(open(args["le"], "rb").read())
encodings=pickle.loads(open(args["encoding"], "rb").read())

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
# start the FPS throughput estimator
fps = FPS().start()
name="unknown"

tolerance = 0.40

conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com",
                               user="bc534e43745e55", password="3db62771", 
                               database="heroku_642c138889636e7")
cursor = conn.cursor()
print("[INFO] CONNEXION BDD SUCCEED")

while True:
	resultat=[]
	frame = vs.read()
	frame = imutils.resize(frame, width=600)
	(h, w) = frame.shape[:2]
	imageBlob = cv2.dnn.blobFromImage(
	cv2.resize(frame, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)
	detector.setInput(imageBlob)
	detections = detector.forward()
	print("[INFO] Visage détecté :")
	print(len(detections))
	if len(detections) > 0:
		box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		# extract the face ROI and grab the ROI dimensions
		face = frame[startY:endY, startX:endX]
		(fH, fW) = face.shape[:2]
		faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96, 96), (0, 0, 0), swapRB=True, crop=False)
		embedder.setInput(faceBlob)
		vec = embedder.forward()
		#print(vec)
		i=0
		for i in range(len(encodings["encodings"])):	
			#print(encodings["names"][i])
			vectors = np.linalg.norm(abs(encodings["encodings"][i]) - abs(vec), axis=1)
			#print("RESULTAT")
			#print(vectors[0])
			resultat.append(vectors[0])
		if(min(resultat)<=tolerance):
			index_name=resultat.index(min(resultat))
			name=encodings["names"][index_name]
		else:
			name="unknown"
		text = "{}".format(name)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		if(name == "unknown"):
			cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
			cv2.putText(frame, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		else:
			cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 255, 0), 2)
			cv2.putText(frame, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
			nom=name.split(" ")
			print(name)
			print(nom[0])
			cursor.execute('UPDATE Etudiant SET Presence=1 WHERE Nom LIKE \'%' + nom[0] + '%\' AND Presence=0')
			#cursor.execute('UPDATE Etudiant SET Presence=0 WHERE Nom LIKE \'%' + nom[0] + '%\' AND Presence=1') #Mettre sur un autre pc
			conn.commit()
		
		
		
	fps.update()
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
cursor.close()
conn.close()
