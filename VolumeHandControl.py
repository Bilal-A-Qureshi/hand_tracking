import cv2
import time as t
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#wCam, hCam = 640,480


cap = cv2.VideoCapture(0)
#cap.set(3,wCam)
#cap.set(4,hCam)
pTime=0
vol=0
vol_bar=400
percent=0


detector = htm.handDetector(detectionCon=0.7)




devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-9, None)

minVol=volumeRange[0]
maxVol=volumeRange[1]



while True:


    success,img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (0, 255, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)

        length = math.hypot(x2-x1,y2-y1)
        #print(length)

        #hand range 50 to 270
        #volume range -65 to 0

        vol = np.interp(length,[50,180],[minVol,maxVol])
        print(int(length),vol)
        vol_bar = np.interp(length, [50, 180], [400,150])

        percent = np.interp(length, [50, 180], [0,100])





        volume.SetMasterVolumeLevel(vol, None)


        if length<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)


    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'vol: {int(percent)}%', (40, 90), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 50, 255), 3)



    cTime = t.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,50),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)


    cv2.imshow("Image",img)
    cv2.waitKey(1)
