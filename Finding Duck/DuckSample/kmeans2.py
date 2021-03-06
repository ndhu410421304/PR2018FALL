import numpy as np
import cv2

import time
start_time = time.time()

#img = cv2.imread('mask.png')
sampleimg = cv2.imread("full_duck.jpg",3)
mask= cv2.imread("Mask.png",3)
maskimg = mask.copy()



m = np.fromfile('mask.dat', dtype=int)
m = np.reshape(m, (-1, 2))

narr = []

print(m.shape[0])

winsize = 49
hwinsize = 24
#pixels duck should comtain
#~472, bias = 200
minduck = 95625
maxduck = 191250
for i in range(m.shape[0]):
	x,y = m[i]
	sx,sy = x,y
	#higher than some value
	s = 0
	for cy in range(49):
		for cx in range(49):
			s = s + maskimg[x-hwinsize + cx][y-hwinsize + cy].sum()

	#prevent redo
	if(((s % 255) == 0) and s != 0):
		if(s > minduck):
			k = 1 + s / maxduck
			k = int(k)
			x2 = x-hwinsize+1
			y2 = y-hwinsize+1
			x3 = x+hwinsize-1
			y3 = y+hwinsize-1
			j1 = 1
			j2 = 1
			n = 1
			#put value from window to array
			arr = []
			arr.append(([x, y]))
			while(j1 == 1):
				if((i-n)<0):
					break
				x,y = m[i-n]
				n = n + 1
				if(x < x2 and y < y2):
					j1 = 0
				else:
					if(x >= x2 and  x3 >= x):
						if(y >= y2 and  y3 >= y):
							arr.append(([x, y]))
			n = 1
			while(j2 == 1):
				if((i+n)>=m.shape[0]):
					break
				x,y = m[i+n]
				n = n + 1
				if(x > x3 and y > y3):
					j1 = 0
				else:
					if(x >= x2 and  x3 >= x):
						if(y >= y2 and  y3 >= y):
							arr.append(([x, y]))
			Z = np.float32(arr)
			#print(arr)

			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
			ret,label,center=cv2.kmeans(Z,k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

			#center = center.astype(int)
			
			for q in range(k):
				if(k == 1):
					b,d = center[q]
					cv2.circle(sampleimg, (d,b), 3, (0,0,255), -1)
					#prevent redo
					#cv2.circle(maskimg, (b,d), 3, (0,0,254), -1)
					maskimg[sx,sy,:] = [254,254,254]
				else:
					b,d = center[q]
					cv2.circle(sampleimg, (d,b), 3, (0,0,255), -1)
					#prevent redo
					#cv2.circle(maskimg, (b,d), 3, (0,0,254), -1)
					maskimg[sx,sy,:] = [254,254,254]

			narr.append(([sx, sy]))
			
print("--- %s seconds ---" % (time.time() - start_time))
cv2.imwrite('KMean2.png', sampleimg)

narr.tofile('narr.dat')
				