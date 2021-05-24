# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import MySQLdb
import time
from datetime import date,datetime
def face_recognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
  
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
   
    db = MySQLdb.connect(host="localhost",user="pi",password="raspberry",db="project",charset='utf8')
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select student_number,name from student")

    

   
    # names related to ids: example ==> loze: id=1,  etc
    # 이런식으로 사용자의 이름을 사용자 수만큼 추가해준다.
    #names = ['None', 'loze', 'ljy', 'chs', 'ksw']
    id=0
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    check=0
    bef=time.time()
    while True:
       
        if(time.time()-bef>=20):
            break
        ret, img =cam.read()
        img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:
           
         
            
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match
            if (check==0 and confidence < 100):
                print("checking..")
                sql = "insert into attendance values(%s,%s,%s)"
                cur.execute(sql,(date.today(),datetime.now(),id))
                #confidence = "  {0}%".format(round(100 - confidence))
                check=1
                db.commit()
            else:
                if(check ==0):
                    id = "unknown"
                    #confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
