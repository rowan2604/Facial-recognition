import os

os.system("python bdd_extraction.py")

os.system("python encodage_faces.py --dataset dataset --encodings output/encodings.pickle --detector face_detection_model --encodings-model openface.nn4.small2.v1.t7")
#Encodage et Reconnaissance des visages

os.system("python train_model.py --encodings output/encodings.pickle --recognizer output/recognizer.pickle --le output/le.pickle")

os.system("python recognize_video.py --detector face_detection_model --en openface.nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle --encoding output/encodings.pickle")

