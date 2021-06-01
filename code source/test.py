import sched,time,os
s = sched.scheduler(time.time, time.sleep)

def launch(sc) :
    # stream=open('Project-Reconnaissance-Facial-abdel/code source/encodage_faces.py')
    # stream2=open('Project-Reconnaissance-Facial-abdel/code source/recognition_faces_video.py')
    # read_file=stream.read()
    # read_file2=stream2.read()
    # # exec(read_file)
    # # exec(read_file2)
    os.system("python encodage_faces.py --i faces -e encodings.pickle")
    os.system("python recognition_faces_video.py -e encodings.pickle --display 1")

    sc.enter( 20, 1, launch, (sc,))

s.enter(20,1,launch, (s,))  
s.run() 