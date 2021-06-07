# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to output model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to output label encoder")
args = vars(ap.parse_args())

# load the face embeddings
print("[INFO] Chargements Des Visages Encodés")
data = pickle.loads(open(args["encodings"], "rb").read())
# encode the labels
print("[INFO] Nom des Visages")
le = LabelEncoder()
labels = le.fit_transform(data["names"]) # Transforme les nom en entier c'est à dire Exemple : Ronaldo son nom devient 0 etc
print(labels)
print("[INFO] Entrainement de L'IA")
recognizer= SVC(C=1.0,kernel="linear", probability=True)
recognizer.fit(data["encodings"], labels)
# write the actual face recognition model to disk
f = open(args["recognizer"], "wb")
f.write(pickle.dumps(recognizer))
f.close()
# write the label encoder to disk
f = open(args["le"], "wb")
f.write(pickle.dumps(le))
f.close()