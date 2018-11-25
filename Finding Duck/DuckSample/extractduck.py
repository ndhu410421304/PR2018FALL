import sys
import cv2 as cv
import numpy as np
import math

class Gmodel:
	def __init__(self):
		self.u = 0
		self.co = 0
		#self.p = 0
	def likelihood(self, r, g, b): #array
		p = 0
		return p
	def callikelihood(self):
		r = 0
		g = 0
		b = 0
		totallikelihood = 0
		for n:
			totallikelihood = totallikelihood + self.likelihood(r,g.b)
		return totallikelihood
		
	def pox(self, r, g, b):
		x = 0
		bias = 1 #3-2
		for n:
			total = total + x
		self.u = total / n
		#np.transpose
		total = 0
		for n:
			total = total + (x - u) * np.transpose(x - u)
		self.co = total / (n - 1) #3-2 bias estimation

class Bayes:
	def __init__(self):
		self.w0 = 1
		self.w1 = 1
	def classify(self, pox1, pox2)
		label = 0
		return label

sampleimg = cv.LoadImage("full_duck.jpg")
duckimg = cv.LoadImage("duckplot.jpg")
nonduckimg = cv.LoadImage("nonduckplot.jpg")		
		
duckb,duckg,duckr = cv.split(duckimg)
nonduckb,nonduckg,nonduckr = cv.split(nonduckimg)
sampleb,sampleg,sampler = cv.split(sampleimg)

ducklisti = []
ducklistj = []
ducknum = 0
for i in range(duckimg.height):
    for j in range(duckimg.width):
        if duckb[i,j] == 0 and duckg[i,j] == 0 and duckr[i,j] == 255:
			ducklisti.append(i)
			ducklistj.append(j)
			ducknum = ducknum + 1

nonducklisti = []
nonducklistj = []
nonducknum = 0
for i in range(nonduckimg.height):
    for j in range(nonduckimg.width):
        if nonduckb[i,j] == 255 and nonduckg[i,j] == 0 and nonduckr[i,j] == 178:
			nonducklisti.append(i)
			nonducklistj.append(j)
			nonducknum = nonducknum + 1


			
for n in range(ducknum):
	startpointi = ducklist[i] - 19
	startpointj = ducklist[j] - 19
	for i in range(39):
		for j in range(39):
			
	
	
		



