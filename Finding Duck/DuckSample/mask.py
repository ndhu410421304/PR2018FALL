import cv2
import numpy as np

#cap = cv2.VideoCapture(0)

img = cv2.imread("Result_extract3.jpg",3)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

print(img[2039,5892])
print(hsv[2039,5892])
print(img[5892,2039])
print(hsv[5892,2039])

dot = np.array([80,240,240])
dot_max = np.array([100,255,255])

mask = cv2.inRange(hsv, dot, dot_max)
#res = cv2.bitwise_and(img,img, mask= mask)

#cv2.imshow('mask',mask)
#cv2.imshow('res',res)

cv2.imwrite('Mask.png', mask)

#cv2.destroyAllWindows()
#img.release()