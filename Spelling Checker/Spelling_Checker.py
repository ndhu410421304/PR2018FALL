#Spelling Checker
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDesktopServices

f = open("dictionary.txt", "r") 
#print(f.read()) 
#print(f.readline())
word = input('Enter your Word:')
print(word)
linenum = 0;
for line in f:
	linenum+=1
print(linenum)