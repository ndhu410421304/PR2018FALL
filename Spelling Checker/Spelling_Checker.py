#Spelling Checker
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDesktopServices
import numpy

f = open("dictionary.txt", "r") 
#print(f.read()) 
#print(f.readline())
D = numpy.zeros((40, 40))
#list
D1 = []
D2 = []
D3 = []
#count length
D1C = 0
D2C = 0
D3C = 0

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
	line = line.replace('\n','')
	B = line
	J = len(line) #because it include changeline character, so -1(old stuff)
	#print(line)
	#print(J)

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
		D3C += 1
	if(Distance == 2):
		D2.append(B)
		D2C += 1
	if(Distance == 1):
		D1.append(B)
		D1C += 1
	if(Distance == 0):
		closestword = B
		equal = 1
		
if(equal == 1):
	print('The spelling is correct!')
else:
	print('Spelling is wrong.')
	print('Word with distance 1:')
	#print(D1)
	for i in range(0,D1C):
		print(D1[i])
	print('Word with distance 2:')
	#print(D2)
	for i in range(0,D2C):
		print(D2[i])
	print('Word with distance 3:')
	#print(D3)
	for i in range(0,D3C):
		print(D3[i])
#print(linenum)