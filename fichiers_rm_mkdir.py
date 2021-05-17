

import os
import keyboard
import sched
import time
import sys
s = sched.scheduler(time.time, time.sleep)
# liste pour les noms des fichiers
List = ["roro", "zebi", "yazebi", "roroeeerr"]
i = 0


def launch(sc):
    while True:
        for i in List:
            if keyboard.read_key() == "r":
                print("You pressed r")
                # si il existe pas on ne le supprime pas car on ne peut pas
                if os.path.exists(str(i)):
                    os.removedirs(str(i))
                    print("Directory ", str(i),  " removed ")
                    # creation du fichier de la liste
                os.mkdir(str(i))
                print("Directory ", str(i),  " Created ")
                # timer de la boucle
        sc.enter(10, 1, launch, (sc,))
        break


# timer avant la premiere exec
s.enter(1, 1, launch, (s,))
s.run()
