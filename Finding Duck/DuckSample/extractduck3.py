import sys
import cv2 as cv
import numpy as np
import math
from numpy.linalg import matrix_power

import time
start_time = time.time()

class Gmodel:
	def __init__(self, img):
		self.img = img
		self.u = np.zeros((1,3))
		self.cov = np.zeros((3,3))
		self.realco = np.zeros((3,3))
		self.sqrealco = np.zeros((3,3))
		self.param2 = np.sqrt(np.power(np.pi,3))
		self.param3 = np.zeros((3,3))
		self.num = 0
		self.buildmodel()
		
		
	def pox(self, x):
		result = np.exp((x - self.u) / (self.realco) * np.transpose(x - self.u) /  (-2)) / self.param3
		#print(result)
		return result.sum()

	def buildmodel(self):
		hid,weid = self.img.shape[:2]
		num = hid*weid
		self.num = num
		self.u = [[self.img[:,:,0].sum(), self.img[:,:,1].sum(), self.img[:,:,2].sum()]]
		self.u = np.divide(self.u, num)
		self.cov = np.zeros((3,3))
		sub = np.subtract(self.img, self.u)
		sub = np.asarray(sub)
		for i in range(np.ndim(sub)): #?
			self.cov = self.cov + (np.transpose(sub[i,:])).dot(sub[i,:]) #?
		self.cov = np.divide(self.cov,num-1)
		self.realco = np.sqrt(self.cov)
		self.sqrealco = np.sqrt(self.realco)
		self.param3 = self.sqrealco * self.param2

class Bayes:
	def __init__(self):
		self.w0 = 1
		self.w1 = 1
	def classify(self, pox1, pox2):
		if(pox1 > pox2):
			label = 1
		else:
			label = 0
		return label

sampleimg = cv.imread("full_duck.jpg",3)
duckimg = cv.imread("slice_duck_2.jpg",3)
nonduckimg = cv.imread("slice_nonduck_1.jpg",3)

duckmodel = Gmodel(duckimg)
nonduckmodel = Gmodel(nonduckimg)

B = Bayes()

im = np.asarray(sampleimg)

#print([*range(0,100000)])

hid,weid = sampleimg.shape[:2]
for i in range(hid):
	for j in range(weid):
		if(B.classify(duckmodel.pox(im[i,j,]),nonduckmodel.pox(im[i,j,])) == 1):
			sampleimg.itemset((i,j,2),255)
			sampleimg.itemset((i,j,2),0)
			sampleimg.itemset((i,j,2),0)
		print(i,j)
print(im[1,1,])
print(im.shape)
#np.apply_along_axis(duckmodel.pox(im), 0, im)
#sd = duckmodel.pox(im[1,1,:])
#nd = nonduckmodel.pox(im[:,:,])


print("--- %s seconds ---" % (time.time() - start_time))
cv.imwrite('Result_extract3.jpg', sampleimg)

			

			
	
	
		



