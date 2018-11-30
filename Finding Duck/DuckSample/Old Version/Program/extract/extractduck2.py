import sys
import cv2 as cv
import numpy as np
import math
from numpy.linalg import matrix_power

import time
start_time = time.time()

class Gmodel:
	#save some steps by save them as variables in the model
	def __init__(self, array, n):
		self.array = array
		self.num = n
		self.resultarray = np.zeros((3,3))
		self.u = np.zeros((1,3))
		self.co = np.zeros((3,3))
		self.realco = np.zeros((3,3))
		self.sqrealco = np.zeros((3,3))
		self.param2 = np.sqrt(np.power(np.pi,3))
		self.param3 = np.zeros((3,3))
	
	#calculation with lighter bureden of calculation
	def pox(self, x):
		result = np.exp((x - self.u) / (self.realco) * np.transpose(x - self.u) /  (-2)) / self.param3
		return result.sum()
	
	#set up array we are going to use for calculation
	def setarray(self,array):
		self.array = array

	#here we get the param meter we are going to use in calculating probability, include mean, cov and other frequntly used ones
	def buildmodel(self):
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

#classify by compare which is greater
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

#load image
sampleimg = cv.imread("full_duck.jpg",3)
duckimg = cv.imread("slice_duck_1.jpg",3)
nonduckimg = cv.imread("slice_nonduck_1.jpg",3)
		
#split with channels
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
		#set value filter for the sampling dots
		if duckb[i,j] > 251 and duckg[i,j] > 251 and duckr[i,j] > 251: #v2-4
		#if duckb[i,j] > 250 and duckg[i,j] > 250 and duckr[i,j] > 250: #v2-3
		#if duckb[i,j] > 240 and duckg[i,j] > 240 and duckr[i,j] > 240: #v2-2
		#if duckb[i,j] > 235 and duckg[i,j] > 235 and duckr[i,j] > 235: #v2-1
			duckarray[n,0] = duckb[i,j]
			duckarray[n,1] = duckg[i,j]
			duckarray[n,2] = duckr[i,j]
		else:
			duckarray[n,0] = 255
			duckarray[n,1] = 255
			duckarray[n,2] = 255
		n = n + 1
		
n = 0
nonducknum = hin * wein
nonduckarray = np.zeros((nonducknum,3))
for i in range(hin):
	for j in range(wein):
		#set value filter for the sampling dots, same as what we do to the ducks
		if nonduckb[i,j] > 210 and nonduckg[i,j] > 210 and nonduckr[i,j] > 210: #v2-4
		#if nonduckb[i,j] > 200 and nonduckg[i,j] > 200 and nonduckr[i,j] > 200: #v2-3
			nonduckarray[n,0] = nonduckb[i,j]
			nonduckarray[n,1] = nonduckg[i,j]
			nonduckarray[n,2] = nonduckr[i,j]
		else:
			#nonduckarray[n,0] = 200
			#nonduckarray[n,1] = 200
			#nonduckarray[n,2] = 200 #v2-3
			nonduckarray[n,0] = 210
			nonduckarray[n,1] = 210
			nonduckarray[n,2] = 210 #v2-4
		n = n + 1

#the code above remoce a pair of for loops, simply by combine them into single one
n = 0
duckmodel = Gmodel(duckarray, ducknum)
nonduckmodel = Gmodel(nonduckarray, nonducknum)
	
#set up array of the result we had gotten	
duckmodel.setarray(duckarray)
nonduckmodel.setarray(nonduckarray)

duckmodel.buildmodel()
nonduckmodel.buildmodel()

#do classification
bayes = Bayes()
test = np.zeros((1,3))

for i in range(hi):
	for j in range(wei):
		#print('5')
		test[0,0] = sampleb[i,j]
		test[0,1] = sampleg[i,j]
		test[0,2] = sampler[i,j]
		#set up dot if the duck had much higher probability on specific dots
		label = bayes.classify(duckmodel.pox(test), nonduckmodel.pox(test))
		if(label):
			color = (0,0,255)
			sampleimg[i,j] = color

print("--- %s seconds ---" % (time.time() - start_time))
cv.imwrite('Result_4.jpg', sampleimg)

			

			
	
	
		



