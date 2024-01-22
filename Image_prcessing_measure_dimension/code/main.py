import cv2
import numpy as np 
import utils

webcam = False
path = '5.jpeg'
# path = 'balok.jpeg'
cap = cv2.VideoCapture(1)
cap.set(10,160)
cap.set(3, 1920)
cap.set(4,1080)


scale = 3
wP = 148*6
hP = 210*scale



while True:
    # input_ = input()
    # if(input_ == 1) : #trigger with input
        success, image = cap.read()
        image , conts = utils.getContours(image, minArea=50000, filter=4)
        if len(conts) != 0:
            biggest = conts[0][2]
            # print(biggest)
            imgWarp = utils.warpImg(image,biggest,wP,hP)
            image_cnt , conts = utils.getContours(imgWarp, minArea=2000, filter=4, cThr=[50,50],draw =False)

            if len(conts) != 0:
                for obj in conts:
                    cv2.polylines(image_cnt,[obj[2]],True,(0,255,0),2)
                    nPoints = utils.reorder(obj[2])
                    nW = round((utils.findDis(nPoints[0][0]//scale, nPoints[1][0]//scale)/10),1)
                    nH = round((utils.findDis(nPoints[0][0]//scale, nPoints[2][0]//scale)/10),1)

                    cv2.arrowedLine(image_cnt, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    cv2.arrowedLine(image_cnt, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    x, y, w, h = obj[3]
                    cv2.putText(image_cnt, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (255, 0, 255), 2)
                    cv2.putText(image_cnt, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (255, 0, 255), 2)
                                
            cv2.imshow('result', image_cnt)
            # check width & height start
            # print("width : ")
            # print(nW)
            # print(" Height :")
            # print(nH, end=" ")
            # print()
            # check width & height end
        else:
            print(len(conts))


        image = cv2.resize(image, (0,0),None,0.5,0.5)
        cv2.imshow('original', image) 
        cv2.waitKey(1) 
        # cv2.destroyAllWindows()
    # else :
    #     print("no input")

