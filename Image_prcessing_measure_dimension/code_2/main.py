# import the opencv library
import cv2
import numpy as np
import time
import serial 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("../code_2/impro-55674-firebase-adminsdk-qt6ir-86bcd1c6eb.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://impro-55674-default-rtdb.firebaseio.com/'
})
arduino = serial.Serial(port='COM14', baudrate=115200, timeout=.1) 

# define a video capture object
frameWidth = 640
frameHeight = 480
vid = cv2.VideoCapture(1)
vid.set(3, frameWidth)
vid.set(4,frameHeight)

def empty(a):
     pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",150,255,empty)
cv2.createTrackbar("Threshold2","Parameters",255,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)
scale = 20

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img,imgContour):
    received = arduino.readline()
    thick = str(received.decode('utf-8'))

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area","Parameters")
        if area> 1000:
            cv2.drawContours(imgContour, cnt, -1,(255,0,255), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # print(len(approx))
            x, y ,w, h = cv2.boundingRect(approx)
            width_ = w*0.0895
            height_ = h*0.0891
            cv2.rectangle(imgContour, (x,y),(x+w,y+h),(0,100,0),3)
            # print("width : " + str(width_) + " Height : " + str(height_) + " Thickness : " + str(thick))
            # print(str(x) + ";" + str(y) + ";" + str(w) + ";" + str(h))

            cv2.putText(imgContour, "Width: " +str(int(width_*10)), (y-10,y+h-25),cv2.FONT_HERSHEY_COMPLEX, .5,(0,0,255), 2)
            cv2.putText(imgContour, "Length: " +str(int(height_*10)), (y-10,y+h-10),cv2.FONT_HERSHEY_COMPLEX, .5,(0,100,255), 2)
            cv2.putText(imgContour, "Thick: " + str(thick), (y-10,y+h+5),cv2.FONT_HERSHEY_COMPLEX, .5,(255,0,0), 2)
            
            if cv2.waitKey(10) & 0xFF == ord('s'):
                send_data = root.child('measurement').push({
                    'length' : height_,
                    'thick' : thick,
                    'width' : width_
                })
        




            



 

root = db.reference()
# data = db.reference().get()
# print(data)


while(True):
    
    ret, frame = vid.read()
    imgContour = frame.copy()
    height,width, channels = frame.shape

    #prepare the crop
    centerX,centerY=int(height/2),int(width/2)
    radiusX,radiusY= int(scale*height/100),int(scale*width/100)

    minX,maxX=centerX-radiusX,centerX+radiusX
    minY,maxY=centerY-radiusY,centerY+radiusY

    cropped = frame[minX:maxX, minY:maxY]

    imgBlur = cv2.GaussianBlur(cropped, (7,7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1,threshold2)
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny,kernel, iterations=1)
    
    getContours(imgDil, cropped)

            


    imgStack = stackImages(0.8,([frame,imgGray,imgCanny],[imgDil,imgContour,cropped]))
    cv2.imshow('frame', imgStack)



    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    


# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
