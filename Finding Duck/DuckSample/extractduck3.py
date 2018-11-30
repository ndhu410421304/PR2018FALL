import sys
import cv2 as cv
import numpy as np
import math
from numpy.linalg import matrix_power

#caluclate time
import time
start_time = time.time()

#build a model for each class
class Gmodel:
	#in initialization we set up some varaible, such as parameter param2 and paramm 3, to support probability function  
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
		
	#return the probability
	def pox(self, x):
		#use those parameter we had used before to improve performance
		result = np.exp((x - self.u) / (self.realco) * np.transpose(x - self.u) /  (-2)) / self.param3
		return result.sum()
	#for a model, first we need to get its mean vector and cov matrix, so we do that thing here
	def buildmodel(self):
		hid,weid = self.img.shape[:2]
		num = hid*weid
		self.num = num
		self.u = [[self.img[:,:,0].sum(), self.img[:,:,1].sum(), self.img[:,:,2].sum()]] #use matrix some for fater approach of sum
		self.u = np.divide(self.u, num)
		self.cov = np.zeros((3,3))
		sub = np.subtract(self.img, self.u)
		sub = np.asarray(sub)
		for i in range(np.ndim(sub)): 
			self.cov = self.cov + (np.transpose(sub[i,:])).dot(sub[i,:])  #calculate cov marix here
		self.cov = np.divide(self.cov,num-1)
		self.realco = np.sqrt(self.cov) #here we save some parameter which is going to do in the future
		self.sqrealco = np.sqrt(self.realco)
		self.param3 = self.sqrealco * self.param2

#compare which ones probability is higher
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

#create model for each class
duckmodel = Gmodel(duckimg)
nonduckmodel = Gmodel(nonduckimg)

#create classifier
B = Bayes()

#sample image array
im = np.asarray(sampleimg)

#for each pixel, if he duck's probability were much higher, we will plot a pixel to blue
hid,weid = sampleimg.shape[:2]
for i in range(hid):
	for j in range(weid):
		if(B.classify(duckmodel.pox(im[i,j,]),nonduckmodel.pox(im[i,j,])) == 1):
			sampleimg.itemset((i,j,2),255)
			sampleimg.itemset((i,j,2),0)
			sampleimg.itemset((i,j,2),0)

#show time run and save the result
print("--- %s seconds ---" % (time.time() - start_time))
cv.imwrite('Result_extract3.jpg', sampleimg)

			

			
	
	
		



