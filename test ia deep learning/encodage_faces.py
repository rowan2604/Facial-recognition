# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to output serialized db of facial encodings")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--encodings-model", required=True,
	help="path to OpenCV's deep learning face encodings model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector from disk
print("[INFO] Chargement Detection De Visage")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# load our serialized face embedding model from disk
print("[INFO] Chargement Reconnaissance Faciale")
embedder = cv2.dnn.readNetFromTorch(args["encodings_model"])

# grab the paths to the input images in our dataset
print ( "[INFO] Création d'une liste de tous les chemins des images" )
imagePaths = list(paths.list_images(args["dataset"]))
# initialize our lists of extracted facial embeddings and
# corresponding people noms
Encodages_visage_connu = []
nom_connu = []
# initialize the count_picture number of faces processed
count_picture = len(imagePaths)

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person nom from the image path
	print("[INFO] Traitement d'image {}/{}".format(i+1,count_picture))
	nom = imagePath.split(os.path.sep)[-2]
	print(nom)
	image = cv2.imread(imagePath)
	imageBlob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)
	detector.setInput(imageBlob)
	detections = detector.forward()
	print("[INFO] Visage détecté :")
	(h, w) = image.shape[:2]
	print(len(detections))
	if len(detections) > 0:
		box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		# extract the face ROI and grab the ROI dimensions
		face = image[startY:endY, startX:endX]
		(fH, fW) = face.shape[:2]
		faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96, 96), (0, 0, 0), swapRB=True, crop=False)
		embedder.setInput(faceBlob)
		vec = embedder.forward()
		#print("[INFO : NOM !!!!!!!!!!]:"+nom)
		#print(vec)
		nom_connu.append(nom)
		Encodages_visage_connu.append(vec.flatten())

print("[INFO] Stockage Données dans encodings.pickle")
data = {"encodings": Encodages_visage_connu, "names": nom_connu}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()

	