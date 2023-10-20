import cv2
import mediapipe as mp 
import time 

cap= cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils


ctime=0
ptime=0
while True:
    success, img=cap.read()
    imgrgb=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                #print(id,lm)
                h, w ,c = img.shape
                #print(w,h)
                cx, cy= int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                #if id==0:
                cv2.circle(img, (cx, cy), 10,(255,0,255),cv2.FILLED)
            mpdraw.draw_landmarks(img, handlms, mphands.HAND_CONNECTIONS)
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break #if insted of 1 i would have written 0 then i would
    #have just got the img of that particular second but writing 1 became a video