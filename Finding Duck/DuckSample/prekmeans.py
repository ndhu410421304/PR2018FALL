import numpy as np
import cv2
import time
start_time = time.time()

img = cv2.imread('Mask.png',1)
hid,weid = img.shape[:2]

arr = []

for i in range(hid):
	for j in range(weid):
		if((img[i,j] == [255,255,255]).all()):
			#append each duck pixel from duck mask to an data for use of k-means later
			arr.append(([i, j]))

nparr = np.array(arr)

print("--- %s seconds ---" % (time.time() - start_time))
#output in dat format
nparr.tofile('mask.dat')

			