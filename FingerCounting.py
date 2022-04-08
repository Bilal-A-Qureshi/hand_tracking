import cv2
import time
import os
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)

folderPath = "images"
myList = os.listdir(folderPath)
print(myList)

overlayList=[]

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

detector = htm.handDetector(detectionCon=0.75)

tipIds=[4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList=detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers=[]

        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):

                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        totalFingers = fingers.count(1)
        print(totalFingers)
        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

        #cv2.rectangle(img,(20,255),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img, str(totalFingers),(15,430),cv2.FONT_HERSHEY_COMPLEX,10,(255,0,0),20)



    cv2.imshow("image",img)
    cv2.waitKey(1)