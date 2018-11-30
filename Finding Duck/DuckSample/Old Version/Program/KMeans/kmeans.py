import numpy as np
import cv2

sampleimg = cv2.imread("full_duck.jpg",3)

#read in mask.dat to plot dot on original image(proved to be wrong in later version)
m = np.fromfile('mask.dat', dtype=int)
m = np.reshape(m, (-1, 2))

Z = np.float32(m)

#do kmeans method
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3000
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center.astype(int)

#use center for plot dots
res = center[label.flatten()]
for i in range(3000):
	b,d = center[i] 
	cv2.circle(sampleimg, (b,d), 3, (0,0,255), -1)

cv2.imwrite('KMean.png', sampleimg)