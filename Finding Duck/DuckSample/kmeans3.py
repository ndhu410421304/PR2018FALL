import numpy as np
import cv2
import time
start_time = time.time()

#get image from mask and original ones
sampleimg = cv2.imread("full_duck.jpg",3)
mask= cv2.imread("Mask.png",3)
maskimg = mask.copy()

#read the data we set in pre kmeans program
m = np.fromfile('mask.dat', dtype=int)
m = np.reshape(m, (-1, 2))

#count numbers of ducks
narr = []

winsize = 49
hwinsize = 24
#pixels duck should comtain(parameters)
minduck = 95625
maxduck = 191250
maxduck2 = 382500
for i in range(m.shape[0]):
	x,y = m[i]
	sx,sy = x,y
	#for a 49 x 49 window, read each "duck point" in this range and to check if the amount of duck is high enough for us to called it a duck
	s = 0
	for cy in range(49):
		for cx in range(49):
			s = s + maskimg[x-hwinsize + cx][y-hwinsize + cy].sum()

	#prevent redo
	if(((s % 255) == 0) and s != 0):
		if(s > minduck):
			k = 1 + s / maxduck2
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
			#apply kmeans method to find the center for ducks
			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
			ret,label,center=cv2.kmeans(Z,k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

			#plot plenty enough dots for each ducks
			for q in range(k):
				if(k == 1):
					b,d = center[q]
					cv2.circle(sampleimg, (d,b), 3, (0,0,255), -1)
					maskimg[sx,sy,:] = [254,254,254]
				else:
					b,d = center[q]
					cv2.circle(sampleimg, (d,b), 3, (0,255,0), -1)
					maskimg[sx,sy,:] = [254,254,254]
			#save data for future
			narr.append(([sx, sy]))
			
print("--- %s seconds ---" % (time.time() - start_time))
cv2.imwrite('KMean3.png', sampleimg)

narr.tofile('narr3.dat')
				