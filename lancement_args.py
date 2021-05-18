

import sched
import time
import os
import keyboard
s = sched.scheduler(time.time, time.sleep)
tmp = 600  # 10min


def launch(sc):
    if keyboard.read_key() == "q":
        tmp=1
    os.system("python encodage_faces.py --i faces -e encodings.pickle")
    os.system("python recognition_faces_video.py -e encodings.pickle --display 1")
    sc.enter(tmp, 1, launch, (sc,))
    


# remplacer le 2 par 600 pour avoir 10 min , temps avant le demarrage
s.enter(2, 1, launch, (s,))
s.run()
