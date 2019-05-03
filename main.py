###################################
###  Author :  Shanu Dey        ###
###  created at: May 1st, 2019  ###
###################################

import cv2
import numpy as np
import urllib.request

#testing video
video = 'test.mp4'

#camera interfac. Here ip_address and port should be replaced with the proper one shown in the android app.
cam_id = 'http://ip_address:port/video' 
 
# add your ip address which is show in the serial monitor
url = 'http://192.168.31.135/LED=' 

# choose a proper interface for testing video, and or ipcamera choose and cam_id
cap = cv2.VideoCapture(cam_id)

value = 'OFF'

while cap.isOpened():
    ret,frame = cap.read()

    if not ret:
        break

    #frame = cv2.resize(frame, (640, 480))

    #frame_test = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #print(frame_test.shape)

    img = frame[:,180:450,:]

    img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(img1,127,255,cv2.THRESH_BINARY_INV)

    img2,countours,hierarchy  = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(img,countours,-1,(255,0,0),3)

    for cnt in countours:
        #print(cnt.shape) ## [num,1,2]
        #print(cnt)
        approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)

        cv2.drawContours(img,[approx],-1,(0,0,255),3)

        number_of_vertices = len(approx)

        x = approx.ravel()[0]
        y = approx.ravel()[0]+180

        if number_of_vertices==4:
            print("fire")
            if value=='OFF':
                value = 'ON'
                try:
                    urllib.request.urlopen(url+value)
                except Exception as e:
                    print(e)

        else:
            print("not fire")
            if value=='ON':
                value = 'OFF'
                try:
                    urllib.request.urlopen(url + value)
                except Exception as e:
                    print(e)

    cv2.rectangle(frame,(180,0),(450,480),(0,255,0),3)

    #cv2.imshow("img", img)
    cv2.imshow("video",frame)


    k = cv2.waitKey(1)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()
