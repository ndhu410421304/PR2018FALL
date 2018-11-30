import sys
import cv2 as cv
import numpy as np
import math
from numpy.linalg import matrix_power

class Gmodel:
	def __init__(self, array, n):
		self.array = array
		self.num = n
		self.resultarray = np.zeros((3,3))
		self.u = np.zeros((1,3))
		self.co = np.zeros((3,3))
	
	#do every caluclation here, which cause program need to do same step again and again
	def pox(self, x):
		realco = np.sqrt(self.co)
		result = (np.exp((x - self.u) / (realco) * np.transpose(x - self.u) /  (-2)) / np.sqrt(realco)) / np.sqrt(np.power(np.pi,3))
		return result.sum()
	
	#set up the value array
	def setarray(self,array):
		self.array = array

	#find mean vector and cov matrix
	def buildmodel(self):
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

#load images all origin and samples
sampleimg = cv.imread("full_duck.jpg",3)
duckimg = cv.imread("duckplot.png",3)
nonduckimg = cv.imread("nonduckplot.png",3)

#split them into multiple channels
duckb,duckg,duckr = cv.split(duckimg)
nonduckb,nonduckg,nonduckr = cv.split(nonduckimg)
sampleb,sampleg,sampler = cv.split(sampleimg)

hi, wei = sampleimg.shape[:2]

#compare if the pixel have the color we paint, if it is we get the pixle of same position from original sample (for every pixels)
ducklisti = []
ducklistj = []
ducknum = 0
for i in range(hi):
	for j in range(wei):
		if duckb[i,j] < 2 and duckg[i,j] < 2 and duckr[i,j] > 235:
			ducklisti.append(i)
			ducklistj.append(j)
			ducknum = ducknum + 1

#do same step to nonduck
nonducklisti = []
nonducklistj = []
nonducknum = 0
for i in range(hi):
	for j in range(wei):
		if nonduckb[i,j] == 255 and nonduckg[i,j] == 0 and nonduckr[i,j] == 178:
			nonducklisti.append(i)
			nonducklistj.append(j)
			nonducknum = nonducknum + 1

#create 2 empty arrays to set the size of model(for initialization
duckarray = np.zeros((ducknum,3))
nonduckarray = np.zeros((nonducknum,3))			

duckmodel = Gmodel(duckarray, ducknum)
nonduckmodel = Gmodel(nonduckarray, nonducknum)

#get the exact value of the postion we get in the last step
for n in range(ducknum):
	startpointi = ducklisti[n] - 0
	startpointj = ducklistj[n] - 0
	for i in range(1):
		for j in range(1):
			duckarray[n,0] = sampleb[startpointj + i, startpointj + j]
			duckarray[n,1] = sampleg[startpointj + i, startpointj + j]
			duckarray[n,2] = sampler[startpointj + i, startpointj + j]
#then set this up to the model
duckmodel.setarray(duckarray)

#do the same thing to non-duck
for n in range(nonducknum):
	startpointi = nonducklisti[n] - 0
	startpointj = nonducklistj[n] - 0
	for i in range(1):
		for j in range(1):
			nonduckarray[n,0] = sampleb[startpointj + i, startpointj + j]
			nonduckarray[n,1] = sampleg[startpointj + i, startpointj + j]
			nonduckarray[n,2] = sampler[startpointj + i, startpointj + j]
nonduckmodel.setarray(nonduckarray)

duckmodel.buildmodel()
nonduckmodel.buildmodel()

#finally we use bayes classification to get the result(for each pxels
bayes = Bayes()
test = np.zeros((1,3))

#do calculation for each channel then combine into aingle tuple and put them in the classifier
for i in range(hi):
	for j in range(wei):
		test[0,0] = sampleb[i,j]
		test[0,1] = sampleg[i,j]
		test[0,2] = sampler[i,j]
		label = bayes.classify(duckmodel.pox(test), nonduckmodel.pox(test))
		if(label):
			color = (0,0,255)
			sampleimg[i,j] = color

#save result
cv.imwrite('Result.jpg', sampleimg)

			

			
	
	
		



