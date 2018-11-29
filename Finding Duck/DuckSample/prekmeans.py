import numpy as np
import cv2
import time
start_time = time.time()

img = cv2.imread('mask.png',1)
hid,weid = img.shape[:2]

#c = np.fromfile('mask.dat', dtype=int)
#c = np.reshape(c, (-1, 2))
#b,d = c[1]
#print(img[b,d])

#print(img[1673,4185])
#print(img[4185,1673])

arr = []

for i in range(hid):
	for j in range(weid):
		if((img[i,j] == [255,255,255]).all()):
			#print('1')
			arr.append(([i, j]))

nparr = np.array(arr)

print("--- %s seconds ---" % (time.time() - start_time))

nparr.tofile('mask.dat')
#print(arr)
			