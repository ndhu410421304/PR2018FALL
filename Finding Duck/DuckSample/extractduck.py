import sys
import cv2 as cv
import numpy as np
import math
from numpy.linalg import matrix_power

class Gmodel:
	def __init__(self, array, n):
		#self.p = 0
		self.array = array
		self.num = n
		self.resultarray = np.zeros((3,3))
		self.u = np.zeros((1,3))
		self.co = np.zeros((3,3))
		
	def pox(self, x):
		realco = np.sqrt(self.co)
		result = (np.exp((x - self.u) / (realco) * np.transpose(x - self.u) /  (-2)) / np.sqrt(realco)) / np.sqrt(np.power(np.pi,3))
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

sampleimg = cv.imread("full_duck_express.jpg",3)
duckimg = cv.imread("duckplot_express_2.png",3)
nonduckimg = cv.imread("nonduckplot_express_2.png",3)
#cv.imshow('S', sampleimg)
#cv.imshow('D', duckimg)
#cv.imshow('N', nonduckimg)
#c = cv.waitKey(12000)		
		
duckb,duckg,duckr = cv.split(duckimg)
nonduckb,nonduckg,nonduckr = cv.split(nonduckimg)
sampleb,sampleg,sampler = cv.split(sampleimg)

hi, wei = sampleimg.shape[:2]

ducklisti = []
ducklistj = []
ducknum = 0
for i in range(hi):
	for j in range(wei):
		if duckb[i,j] == 0 and duckg[i,j] == 0 and duckr[i,j] == 255:
			#print('1')
			ducklisti.append(i)
			ducklistj.append(j)
			ducknum = ducknum + 1

nonducklisti = []
nonducklistj = []
nonducknum = 0
for i in range(hi):
	for j in range(wei):
		if nonduckb[i,j] == 255 and nonduckg[i,j] == 0 and nonduckr[i,j] == 178:
			#print('2')
			nonducklisti.append(i)
			nonducklistj.append(j)
			nonducknum = nonducknum + 1

duckarray = np.zeros((ducknum,3))
nonduckarray = np.zeros((nonducknum,3))			

duckmodel = Gmodel(duckarray, ducknum)
nonduckmodel = Gmodel(nonduckarray, nonducknum)
			
for n in range(ducknum):
	startpointi = ducklisti[n] - 2
	startpointj = ducklistj[n] - 2
	for i in range(5):
		for j in range(5):
			#print('3')
			duckarray[n,0] = sampleb[startpointj + i, startpointj + j]
			duckarray[n,1] = sampleg[startpointj + i, startpointj + j]
			duckarray[n,2] = sampler[startpointj + i, startpointj + j]
duckmodel.setarray(duckarray)

for n in range(nonducknum):
	startpointi = nonducklisti[n] - 0
	startpointj = nonducklistj[n] - 0
	for i in range(1):
		for j in range(1):
			#print('4')
			nonduckarray[n,0] = sampleb[startpointj + i, startpointj + j]
			nonduckarray[n,1] = sampleg[startpointj + i, startpointj + j]
			nonduckarray[n,2] = sampler[startpointj + i, startpointj + j]
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

#cv.ShowImage('Result', sampleimg)
cv.imwrite('Result_express.png', sampleimg)

			

			
	
	
		



