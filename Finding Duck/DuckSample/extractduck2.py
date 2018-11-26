import sys
import cv2 as cv
import numpy as np
import math
from numpy.linalg import matrix_power

import time
start_time = time.time()

class Gmodel:
	def __init__(self, array, n):
		#self.p = 0
		self.array = array
		self.num = n
		self.resultarray = np.zeros((3,3))
		self.u = np.zeros((1,3))
		self.co = np.zeros((3,3))
		self.realco = np.zeros((3,3))
		self.sqrealco = np.zeros((3,3))
		self.param2 = np.sqrt(np.power(np.pi,3))
		self.param3 = np.zeros((3,3))
		
	def pox(self, x):
		result = np.exp((x - self.u) / (self.realco) * np.transpose(x - self.u) /  (-2)) / self.param3
		#print(result)
		return result.sum()
		
	def setarray(self,array):
		self.array = array

	def buildmodel(self):
		#sampleimg = cv.LoadImage("full_duck.jpg")
		#sampleb,sampleg,sampler = cv.split(sampleimg)
		total = np.zeros((1,3))
		for i in range(self.num):
			total = total + self.array[i,:]
		self.u = total / self.num
		for i in range(self.num):
			self.resultarray = self.resultarray + self.array[i,:].dot(np.transpose(self.array[i,:]))
		self.co = self.resultarray / (self.num-1)
		self.realco = np.sqrt(self.co)
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
duckimg = cv.imread("slice_duck_1.jpg",3)
nonduckimg = cv.imread("slice_nonduck_1.jpg",3)
#cv.imshow('S', sampleimg)
#cv.imshow('D', duckimg)
#cv.imshow('N', nonduckimg)
#c = cv.waitKey(12000)		
		
duckb,duckg,duckr = cv.split(duckimg)
nonduckb,nonduckg,nonduckr = cv.split(nonduckimg)
sampleb,sampleg,sampler = cv.split(sampleimg)

hi, wei = sampleimg.shape[:2]

hid,weid = duckimg.shape[:2]
hin,wein = nonduckimg.shape[:2]

n = 0
ducknum = hid * weid
duckarray = np.zeros((ducknum,3))
for i in range(hid):
	for j in range(weid):
		if duckb[i,j] > 235 and duckg[i,j] > 235 and duckr[i,j] > 235:
			duckarray[n,0] = duckb[i,j]
			duckarray[n,1] = duckg[i,j]
			duckarray[n,2] = duckr[i,j]
		else:
			duckarray[n,0] = 250
			duckarray[n,1] = 250
			duckarray[n,2] = 250
		n = n + 1
		
n = 0
nonducknum = hin * wein
nonduckarray = np.zeros((nonducknum,3))
for i in range(hin):
	for j in range(wein):
		nonduckarray[n,0] = nonduckb[i,j]
		nonduckarray[n,1] = nonduckg[i,j]
		nonduckarray[n,2] = nonduckr[i,j]
		n = n + 1

n = 0
duckmodel = Gmodel(duckarray, ducknum)
nonduckmodel = Gmodel(nonduckarray, nonducknum)
			
duckmodel.setarray(duckarray)
nonduckmodel.setarray(nonduckarray)

duckmodel.buildmodel()
nonduckmodel.buildmodel()

bayes = Bayes()
test = np.zeros((1,3))

for i in range(hi):
	for j in range(wei):
		#print('5')
		test[0,0] = sampleb[i,j]
		test[0,1] = sampleg[i,j]
		test[0,2] = sampler[i,j]
		#print(test)
		#print(ducknum)
		label = bayes.classify(duckmodel.pox(test), nonduckmodel.pox(test))
		if(label):
			color = (0,0,255)
			sampleimg[i,j] = color
		n = n + 1
		if(n == 100):
			print(n)
		if((n%10000 == 0) and (n > 10000)):
			print(n)

#cv.ShowImage('Result', sampleimg)
print("--- %s seconds ---" % (time.time() - start_time))
cv.imwrite('Result.jpg', sampleimg)

			

			
	
	
		



