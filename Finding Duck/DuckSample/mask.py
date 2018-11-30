import cv2
import numpy as np

img = cv2.imread("Result_extract3.jpg",3)
#first convert the color sapce from RGB to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#for dot in this rang(light blue),
dot = np.array([80,240,240])
dot_max = np.array([100,255,255])

#will be turn into mask, whihc only contain whte and black
mask = cv2.inRange(hsv, dot, dot_max)

cv2.imwrite('Mask.png', mask)
