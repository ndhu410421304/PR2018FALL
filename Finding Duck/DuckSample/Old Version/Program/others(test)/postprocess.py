import sys
import cv2 as cv
import numpy as np
sys.setrecursionlimit(2000)

import time
start_time = time.time()

out = cv.imread("full_duck.jpg",3)
Re = cv.imread("Result.jpg",3)
Re2 = cv.imread("Result_2.jpg",3)
Re3 = cv.imread("Result_3.jpg",3)
Re4 = cv.imread("Result_4.jpg",3)

b3,g3,r3 = cv.split(Re3)

hi1, wei1 = Re.shape[:2]
hi2, wei2 = Re2.shape[:2]
hi3, wei3 = Re3.shape[:2]
hi4, wei4 = Re4.shape[:2]


class Guess:
	def __init__(self,img,out, hi, wei, b, g, r):
		self.total = 0
		self.img = img
		self.imgb, self.imgg,self.imgr = b,g,r
		self.itotal = 0
		self.jtotal = 0
		self.value = 450
		self.outimg = out
		self.outimgb,self.outimgg,self.outimgr = cv.split(self.outimg)
		self.hi = hi
		self.wei = wei
		self.winsize = 30
		self.array = np.zeros((hi,wei))
	#try to use a big recursive program to run through each pixle but it was taking to much time to use(original method)
	def go(self, i, j, total, las):
		self.total = total
		self.itotal = 0
		self.jtotal = 0
		if(i < self.hi - 30):
			if(j < self.wei - 30):
				if(i == 0 and j == 0):
					for i3 in range(30):
						for j3 in range(30):
							if(self.imgr[i3,j3] > 245):
								self.total += 1
								if(i3 < 30 and j3 == 0):
									self.jtotal += 1
								elif(j3 < 30 and i3 == 0):
									self.itotal += 1
							elif(self.imgb[i3,j3] > 245 and self.imgg[i3,j3] > 245 and self.imgr[i3,j3] > 245):
								self.total += 1
								if(i3 < 30 and j3 == 0):
									self.jtotal += 1
								elif(j3 < 30 and i3 == 0):
									self.itotal += 1
				else:
					if(las == 1):
						for j3 in range (30) :
							if(self.imgr[i,j+j3] > 245):
								self.itotal += 1
							elif(self.imgb[i,j+j3] > 245 and self.imgg[i,j+j3] > 245 and self.imgr[i,j+j3] > 245):
								self.itotal += 1
							if(self.imgr[i+30, j+j3] > 245):
								self.total +=1
							elif(self.imgb[i+30,j+j3] > 245 and self.imgg[i+30,j+j3] > 245 and self.imgr[i+30,j+j3] > 245):
								self.total +=1
						for i3 in range (30) :
							if(self.imgr[i+i3,j] > 245):
								self.jtotal += 1
							elif(self.imgb[i+i3,j]  > 245 and self.imgg[i+i3,j] >245 and self.imgr[i+i3,j]>245):
								self.jtotal += 1
					elif(las == 2):
						for j3 in range (30) :
							if(self.imgr[i,j+j3] > 245):
								self.itotal += 1
							elif(self.imgb[i,j+j3] > 245 and self.imgg[i,j+j3] > 245 and self.imgr[i,j+j3] > 245):
								self.itotal += 1
						for i3 in range (30) :
							if(self.imgr[i+i3,j] > 245):
								self.total += 1
							elif(self.imgb[i+i3,j]  > 245 and self.imgg[i+i3,j] >245 and self.imgr[i+i3,j]>245):
								self.total += 1
							if(self.imgr[i+i3,j+30] > 245):
								self.total += 1
							elif(self.imgb[i+i3,j+30]  > 245 and self.imgg[i+i3,j+30] >245 and self.imgr[i+i3,j+30]>245):
								self.total += 1
				
				if(total > self.value):
					self.outimgr[i+15,j+15] = 0
					self.outimgr[i+15,j+15] = 0
					self.outimgr[i+15,j+15] = 255
				
		return total - self.jtotal # ignore most left since they are simply pure black
	
	#use forgo to replace go, though it need to go through every pixeks
	def forgo(self):
		
		for i in range(self.hi):
			for j in range(self.wei):
				if(i == 0 and j == 0):
					self.array[0,0] = self.go(0,0,0,0)
				elif(j != 0):
					self.array[i,j] = self.go(i,j,self.array[i,j-1],1)
				else:
					self.array[i,0] = self.go(i,j,self.array[i-1,j],2)
				print(i,j)
		return self.outimg

#code was simple but class not		
guess3 = Guess(Re3,out,hi3,wei3,b3,g3,r3)
re3img = guess3.forgo()
cv.imwrite('Re3.jpg',re3img)
print("--- %s seconds ---" % (time.time() - start_time))
							
					
		
	