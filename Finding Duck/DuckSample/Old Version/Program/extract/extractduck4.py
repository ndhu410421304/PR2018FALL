import sys
import cv2 as cv
import numpy as np
import math
from numpy.linalg import matrix_power
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

#track time
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
		
	#simply only use the build-in function
	def pox(self, x):
		result = multivariate_normal.pdf(x,self.u.ravel(), self.cov)
		return result
	
	#get mean vectir and cov matrix
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

		#check which's probability is higher
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

#read in images
sampleimg = cv.imread("full_duck.jpg",3)
maskimg = cv.imread("full_duck.jpg",3)
duckimg = cv.imread("slice_duck_2.jpg",3)
nonduckimg = cv.imread("slice_nonduck_1.jpg",3)

#models for each class
duckmodel = Gmodel(duckimg)
nonduckmodel = Gmodel(nonduckimg)

B = Bayes()

im = np.asarray(sampleimg)

#go for each pixel to check for evaluate the result
hid,weid = sampleimg.shape[:2]
for i in range(hid):
	for j in range(weid):
		if(B.classify(duckmodel.pox(im[i,j,]),nonduckmodel.pox(im[i,j,])) == 1):
			#try to use different ways to plot: use itemset this time
			sampleimg.itemset((i,j,0),255)
			sampleimg.itemset((i,j,1),0)
			sampleimg.itemset((i,j,2),0)
			#plot mask at the same time
			maskimg.itemset((i,j,0),255)
			maskimg.itemset((i,j,1),255)
			maskimg.itemset((i,j,2),255)
		else:
			maskimg.itemset((i,j,0),0)
			maskimg.itemset((i,j,1),0)
			maskimg.itemset((i,j,2),0)

print("--- %s seconds ---" % (time.time() - start_time))
cv.imwrite('Result_extract4.jpg', sampleimg)
cv.imwrite('Mask_extract4.png', maskimg)

			

			
	
	
		



