import sys
import cv2 as cv
import numpy as np
import math

class Gmodel:
	def __init__(self, array, n):
		self.u = 0
		self.co = 0
		#self.p = 0
		self.array = array
		self.num = n
		self.resultarray = np.zeros((n,n))
		
	def pox(self, x):
		result = math.exp((x - self.u) * (x - self.u) / (self.co * 2)) / (math.sqrt(2 * math.pi * self.co))
		return result
		
	def setarray(self,array):
		self.array = array

	def buildmodel(self):
		#sampleimg = cv.LoadImage("full_duck.jpg")
		#sampleb,sampleg,sampler = cv.split(sampleimg)
		total = [0,0,0]
		for i in range(self.num):
			total = total + self.array(n,)
		self.u = total / n
		for i in range(self.num):
			resultarray = resultarray + self.array[n,:].dot(np.transpose(self.array[n,:]))
		self.co = resultarray / (n-1)

class Bayes:
	def __init__(self):
		self.w0 = 1
		self.w1 = 1
	def classify(self, pox1, pox2):
		if(pox1 > pox2):
			label = 1
		label = 0
		return label

sampleimg = cv.imread("full_duck_express.jpg",3)
duckimg = cv.imread("duckplot_express.jpg",3)
nonduckimg = cv.imread("nonduckplot_express.jpg",3)
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
			print('1')
			ducklisti.append(i)
			ducklistj.append(j)
			ducknum = ducknum + 1

nonducklisti = []
nonducklistj = []
nonducknum = 0
for i in range(hi):
	for j in range(wei):
		if nonduckb[i,j] == 255 and nonduckg[i,j] == 0 and nonduckr[i,j] == 178:
			print('2')
			nonducklisti.append(i)
			nonducklistj.append(j)
			nonducknum = nonducknum + 1

duckarray = np.zeros((n,3))
nonduckarray = np.zeros((n,3))			

duckmodel = gmodel(duckarray, n)
nonduckmodel = gmodel(nonduckarray, n)
			
for n in range(ducknum):
	startpointi = ducklist[i] - 4
	startpointj = ducklist[j] - 4
	for i in range(9):
		for j in range(9):
			print('3')
			duckarray[n,0] = sampleb[startpointj + i, startpointj + j]
			duckarray[n,1] = sampleg[startpointj + i, startpointj + j]
			duckarray[n,2] = sampler[startpointj + i, startpointj + j]
duckmodel.setarray(array)

for n in range(nonducknum):
	startpointi = nonducklist[i] - 2
	startpointj = nonducklist[j] - 2
	for i in range(5):
		for j in range(5):
			print('4')
			nonduckarray[n,0] = sampleb[startpointj + i, startpointj + j]
			nonduckarray[n,1] = sampleg[startpointj + i, startpointj + j]
			nonduckarray[n,2] = sampler[startpointj + i, startpointj + j]
nonduckmodel.setarray(array)

duckmodel.buildmodel()
nonduckmodel.buildmodel()

bayes = Bayes()
test = np.zeros((1,3))

for i in range(hi):
	for j in range(wei):
		print('5')
		test[0,0] = sampleimgb[i,j]
		test[0,1] = sampleimgg[i,j]
		test[0,2] = sampleimgr[i,j]
		label = bayes.Classify(duckmodel.pox(test), nonduckmodel.pox(test))
		if(label):
			color = (0,0,255)
			sampleimg[i,j] = color

#cv.ShowImage('Result', sampleimg)
cv.imwrite('Result', sampleimg)

			

			
	
	
		



