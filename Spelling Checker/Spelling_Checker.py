#Spelling Checker
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDesktopServices
import numpy

f = open("dictionary.txt", "r") 
#print(f.read()) 
#print(f.readline())
D = numpy.zeros((40, 40))
D1 = []
D2 = []
D3 = []

word = input('Enter your Word:')
#print(word)
minDistance = 10000 #big enough when initial
closestword = word
equal = 0
#print(len(word))
I = len(word)
linenum = 0;
for line in f:
	linenum+=1
	A = word
	B = line
	J = len(line) - 1 #because it include changeline character, so -1

	if(A[0] == B[0]):
		D[0][0] = 0
	else:
		D[0][0] = 1
	for i in range(1,I):
		D[i][0]=D[i-1][0] + 1
	for j in range(1,J):
		D[0][j]=D[0][j-1] + 1
	for i in range(1,I):
		for j in range(1,J):
			c1 = 0
			#print(i,j)
			if(A[i] == B[j]):
				c1 = D[i-1][j-1] + 0
			else:
				c1 = D[i-1][j-1] + 1
			c2 = D[i-1][j] + 1
			c3 = D[i][j-1] + 1
			D[i,j] = min(c1, c2, c3)

	Distance = D[I-1,J-1]
	#if(Distance < minDistance):
		#minDistance = Distance
		#closestWord = B
	
		#print(B)
		#print(minDistance)
	if(Distance == 3):
		D3.append(B)
	if(Distance == 2):
		D2.append(B)
	if(Distance == 1):
		D1.append(B)
	if(Distance == 0):
		closestword = B
		equal = 1
		
if(equal == 1):
	print('The spelling is correct!')
else:
	print('Spelling is wrong.')
	print('Word with distance 1:')
	print(D1)
	print('Word with distance 2:')
	print(D2)
	print('Word with distance 3:')
	print(D3)
#print(linenum)