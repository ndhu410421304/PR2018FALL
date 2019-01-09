#Spelling Checker
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDesktopServices
import numpy

f = open("dictionary.txt", "r") 
#print(f.read()) 
#print(f.readline())
D = numpy.zeros((40, 40))
word = input('Enter your Word:')
print(word)
minDistance = 10000 #big enough when initial
closestword = word
#print(len(word))
I = len(word)
linenum = 0;
for line in f:
	linenum+=1
	A = word
	B = line
	J = len(line)
	D[0][0] = 0
	for i in range(1,I-1):
		D[i][0]=D[i-1][0] + 1
	for j in range(1,J-1):
		D[0][j]=D[0][j-1] + 1
	for i in range(1,I-1):
		for j in range(1,J-1):
			c1 = 0
			print(i,j)
			if(A[i] == B[j]):
				c1 = D[i-1][j-1] + 0
			else:
				c1 = D[i-1][j-1] + 1
			c2 = D[i-1][j] + 1
			c3 = D[i][j-1] + 1
			D[i,j] = min(c1, c2, c3)
	Distance = D[I-1,J-1]
	if(Distance < minDistance):
		minDistance = Distance
		closestWord = B
print(closestWord)
	
print(linenum)