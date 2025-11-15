import cv2 as cv 
import numpy as np
from PIL import Image
cap=cv.VideoCapture(0)
while True:
    ret,frame=cap.read()
    frame=cv.resize(frame,(1000,500))
    hsv_frame=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    lower=np.array([20,100,100])
    upper_bound=np.array([40,255,255])
    mask=cv.inRange(hsv_frame,lower,upper_bound)
    maske_pillow=Image.fromarray(mask)
    boxe=maske_pillow.getbbox() 
    
    if boxe is not None:
        x1,y1,x2,y2=boxe
        cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),10)
        print(boxe)
    cv.imshow('Video',frame)
    if cv.waitKey(1)==ord('q'):
        break
cap.release()
cv.destroyAllWindows()

