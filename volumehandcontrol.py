import time 
import numpy as np 
import handtrackmodule as htm
import cv2
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()


minvol=volrange[0]
maxvol=volrange[1]

cap=cv2.VideoCapture(0)
ptime=0
ctime=0
vol=0
volbar=400
detector = htm.handDetector()
while True:
    success,img=cap.read()
    img = detector.findHands(img)
    lmlist=detector.findPosition(img, draw=False)
    if len(lmlist)!=0:
       #print(lmlist[4],lmlist[8])

       x1,y1=lmlist[4][1],lmlist[4][2]
       x2,y2=lmlist[8][1],lmlist[8][2]
       cx,cy=(x1+x2)//2, (y1+y2)//2

       cv2.circle(img,(x1,y1), 10, (255,0,255), cv2.FILLED)
       cv2.circle(img,(x2,y2), 10, (255,0,255), cv2.FILLED)
       cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
       cv2.circle(img,(cx,cy), 10, (255,0,255), cv2.FILLED)
       
       length=math.hypot((x2-x1), (y2-y2))
       #print(length)
        
       #hand range 10 - 300
       #vol range -65 - 0 

       vol=np.interp(length,[10,120], [minvol,maxvol])
       volbar=np.interp(length,[30,200], [400,150])
       print(length,vol)
       volume.SetMasterVolumeLevel(vol, None)
       if length<10:
        cv2.circle(img,(cx,cy), 10, (0,255,0), cv2.FILLED)
    cv2.rectangle(img,(50,150), (85,400),(255,0,0), 3)
    cv2.rectangle(img,(50,int(volbar)), (85,400),(255,0,0), cv2.FILLED)
       



    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
