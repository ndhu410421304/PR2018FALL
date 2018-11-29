import numpy as np
import cv2

#img = cv2.imread('mask.png')
sampleimg = cv2.imread("full_duck.jpg",3)
maskimg = cv2.imread("mask.png",3)



m = np.fromfile('mask.dat', dtype=int)
m = np.reshape(m, (-1, 2))

print(m.shape[0])

winsize = 49
hwinsize = 24
#pixels duck should comtain
#~472, bias = 200
minduck = 191250
maxduck = 382500
for i in range(m.shape[0]):
	x,y = m[i]
	#higher than some value
	s = maskimg[(x-hwinsize+1):(x+hwinsize-1)][(y-hwinsize+1):(y+hwinsize-1)].sum()
	#prevent redo
	if (s % 255) == 0:
		if(s > 250):
			k = s / maxduck
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
			while(j1):
				x,y = m[i-n]
				n = n + 1
				if(x < x2 and y < y2):
					j1 = 0
				else:
					if(x <= x2 and  x3 <= x):
						if(y <= y2 and  y3 <= y):
							arr.append(([x, y]))
			n = 1
			while(j2):
				x,y = m[i+n]
				n = n + 1
				if(x > x3 and y > y3):
					j1 = 0
				else:
					if(x <= x2 and  x3 <= x):
						if(y <= y2 and  y3 <= y):
							arr.append(([x, y]))
			Z = np.float32(arr)

			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
			ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

			center = center.astype(int)
			
			for q in range(k):
				if(k == 1):
					b,d = center[q]
					cv2.circle(sampleimg, (b,d), 3, (0,0,255), -1)
					#prevent redo
					cv2.circle(maskimg, (x,y), 3, (0,0,254), -1)
				else:
					b,d = center[q]
					cv2.circle(sampleimg, (b,d), 3, (0,0,255), -1)
					#prevent redo
					cv2.circle(maskimg, (x,y), 3, (0,0,254), -1)

cv2.imwrite('KMean2.png', sampleimg)
				