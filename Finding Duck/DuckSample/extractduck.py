import sys
import cv2 as cv
import numpy as np
import math

class Gmodel:
	def __init__(self):
		self.u = 0
		self.co = 0
		#self.p = 0
	def likelihood(self, r, g, b):
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
		
		

class Bayes:
	def __init__(self):
		self.w0 = 1
		self.w1 = 1
	def classify(self, pox1, pox2)
		label = 0
		return label
		



