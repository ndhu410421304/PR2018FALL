import sys
import cv2 as cv
import numpy as np

out = cv.imread("full_duck.jpg",3)
Re = cv.imread("Result.jpg",3)
Re2 = cv.imread("Result_2.jpg",3)
Re3 = cv.imread("Result_3.jpg",3)
Re4 = cv.imread("Result_4.jpg",3)

hi1, wei1 = Re1.shape[:2]
hi2, wei2 = Re2.shape[:2]
hi3, wei3 = Re3.shape[:2]
hi4, wei4 = Re1.shape[:2]

class Guess:
	def __init__(self,out):
		self.total = 0
		self.imgb = []
		self.imgg = []
		self.imgr = []
		self.itotal = 0
		self.value = 450
		self.outimg = out
	def go(self, i, j, total, las):
		self.total = total
		self.itotal = 0
		self.jtotal = 0
		if(i < self.hi - 30):
			if(j < self.j - 30):
				if(i == 0 and j == 0):
					for(i3 in range(30)):
						for(j3 in range(30)):
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
						for(j3 in range 30):
							if(self.imgr[i,j+j3] > 245):
								self.itotal += 1
							elif(self.imgb[i,j+j3] > 245 and self.imgg[i,j+j3] > 245 and self.imgr[i,j+j3] > 245):
								self.itotal += 1
							if(self.imgr[i+30, j+j3] > 245):
								self.total +=1
							elif(self.imgb[i+30,j+j3] > 245 and self.imgg[i+30,j+j3] > 245 and self.imgr[i+30,j+j3] > 245):
								self.total +=1
						for(i3 in range 30):
							if(self.imgr[i+i3,j] > 245):
								self.jtotal += 1
							elif(self.imgb[i+i3,j]  > 245 and self.imgg[i+i3,j] >245 and self.imgr[i+i3,j]>245):
								self.jtotal += 1
					elif(las == 2):
						for(j3 in range 30):
							if(self.imgr[i,j+j3] > 245):
								self.itotal += 1
							elif(self.imgb[i,j+j3] > 245 and self.imgg[i,j+j3] > 245 and self.imgr[i,j+j3] > 245):
								self.itotal += 1
						for(i3 in range 30):
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
				self.go(i + 1, j, total - itotal, 1) #how much to jump if total > value?
				self.go(i, j + 1, total - jtotal, 2)
							
					
		
	