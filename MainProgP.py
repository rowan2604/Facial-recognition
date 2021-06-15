import os

os.system("python bdd_extraction.py")
os.system("python encodage_faces.py --i bdd_picture -e encodings.pickle")
os.system("python recognition_faces_video_present.py -e encodings.pickle --display 1")
#Nous permet de lancer grâce à des commandes systèmes tous les script dans le bonne ordre