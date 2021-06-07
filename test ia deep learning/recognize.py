# import the necessary packages
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
import collection

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-e", "--en", required=True,
	help="path to OpenCV's deep learning face encodings model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
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

#Image où on va vouloir reconnaitre
image = cv2.imread(args["image"])
(h, w) = image.shape[:2] 
imageBlob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)

#Application de l'algorithme de deep learning face detector pour localiser un visage
name="unknown"
resultat=[]
tolerance = 0.7



detector.setInput(imageBlob)
detections = detector.forward()
print("[INFO] Visage détecté :")
print(len(detections))
(h, w) = image.shape[:2]
if len(detections) > 0:
	box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
	(startX, startY, endX, endY) = box.astype("int")
	# extract the face ROI and grab the ROI dimensions
	face = image[startY:endY, startX:endX]
	(fH, fW) = face.shape[:2]
	faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96, 96), (0, 0, 0), swapRB=True, crop=False)
	embedder.setInput(faceBlob)
	vec = embedder.forward()
	print(vec)
	#for i in range(len(encodings["encodings"])):	
		#if(np.allclose(vec,encodings["encodings"][i])):
			#print(encodings["names"][i]+" est la personne sur la photo")
			#name=encodings["names"][i]
			#break
		#else:
			#print(encodings["names"][i]+" n'est pas la personne sur la photo")
	for i in range(len(encodings["encodings"])):	
		print(encodings["names"][i])
		vectors = np.linalg.norm(abs(encodings["encodings"][i]) - abs(vec), axis=1)
		print(vectors[0])
		resultat.append(vectors[0])
	if(min(resultat)<=tolerance):
		index_name=resultat.index(min(resultat))
		name=encodings["names"][index_name]
	text = "{}".format(name)
	y = startY - 10 if startY - 10 > 10 else startY + 10
	cv2.rectangle(image, (startX, startY), (endX, endY),(0, 0, 255), 2)
	cv2.putText(image, text, (startX, y),
	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
	
	

	




		