import cv2 
image=cv2.imread('image.png')
print(image.shape)
image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image=cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
cv2.imshow('Imgae',image)
cv2.waitKey(0)