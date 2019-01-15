#Paragraph Spelling Checker
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
#from PyQt5.QtGui import QApplication #for update progress bar
import numpy

class MainWind(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		#setup
		self.setGeometry(350, 350, 500, 500)
		self.setWindowTitle('Spelling Checker')
		
		#UI of Spelling Checker
		panel = SpellCheckGUI()
		panel.setParent(self)
		self.setCentralWidget(panel) # resize option

		#show the window
		self.show()
		
class SpellCheckGUI(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()
		self.f = open("dictionary.txt", "r") 
		self.D = numpy.zeros((40, 40))
		#list
		self.D1 = []
		self.D2 = []
		self.D3 = []
		#count length
		self.D1C = 0
		self.D2C = 0
		self.D3C = 0

		self.sentence = 'I am ampple.'
		self.word = 'Something'
		self.minDistance = 10000 #big enough when initial
		self.closestword = self.word
		self.equal = 0
		
		self.s_count = 0
		
		#for paragraph record
		self.markrecord = [] # record whether it contain other character at the end(most of the time case)
		self.upperrecord = [] # record first character were upper case or not
		self.wordrecord = [] #record everyword
		
		#for waiting result
		self.pressed = 0
		self.globalword = 'Something'

	def initUI(self):
		self.setGeometry(0,0,500,500)
		grid = QGridLayout()
		
		self.msg = QLabel()
		self.msg.setText("Type in the paragraph you want to check spelling.")
		self.msg.setAlignment(Qt.AlignLeft)
		grid.addWidget(self.msg, 0,1,0,2)
		
		self.lbox = QTextEdit()
		grid.addWidget(self.lbox, 2,1,2,2)
		
		Sbutton = QPushButton('Check')
		Sbutton.clicked.connect(self.press)
		Sbutton.setStyleSheet("QPushButton {font: bold; background-color: white;font-size: 24px;}") #initial button
		grid.addWidget(Sbutton, 4,1,4,2)
		
		self.tbox = QTextEdit()
		grid.addWidget(self.tbox, 8,1,8,2)
		#self.tbox.insertPlainText('abcde')
		
		self.setLayout(grid) #put them all in layout
		self.show()
		
	def press(self):
		#clear Textbox first
		self.tbox.clear()
		
		self.sentence = self.lbox.toPlainText() #need to convert Qstirng to normal string!! (important)
		self.split_paragraph()
		self.s_count = 0 #reset
			
	def split_paragraph(self):
		s_split = self.sentence.split()
		
		#progress bar
		progress = QProgressDialog(self)
		progress.setWindowTitle("Wait a bit...")
		progress.setLabelText("Checking Result...")
		progress.setCancelButtonText("Cancel Output")
		progress.setWindowModality(Qt.WindowModal)
		
		progress.setRange(0,len(s_split))
		
		for spl in s_split:
			progress.setValue(self.s_count)
			QApplication.processEvents() 
			if progress.wasCanceled():
				QMessageBox.warning(self,"Warning","Output Canceled")
				break #break when the checking had beend canceld by user
			#mark 
			mark = 0
			if('.' in spl):
				mark = 1
			elif(',' in spl):
				mark = 2
			elif('?' in spl):
				mark = 3
			elif('!' in spl):
				mark = 4
			elif('"' in spl):
				mark = 5
			self.markrecord.append(mark)
			
			#upper
			upper = 0
			if(spl.istitle()):
				upper = 1
			self.upperrecord.append(upper)
			
			self.s_count += 1
				
			#self.wordrecord.append(self.do_action(strip_charcter(spl))
			self.return_result(self.do_action(self.strip_character(spl)))
		else:
			progress.setValue(self.s_count)
			QMessageBox.information(self,"Done","Output done")
			
			
		#self.return_result()
		
	def strip_character(self,word):
		word = word.replace(',', '')
		word = word.replace('.', '')
		word = word.replace('?', '')
		word = word.replace('!', '')
		word = word.replace('"', '')
		word = word.lower()
		return word
		
	def return_result(self,word):
		
		#word = self.wordrecord[i]
		if(self.upperrecord[self.s_count - 1] == 1): #back to uppercase
			word = word.capitalize()
			#self.wordrecord[self.s_count - 1] = word
		if(self.markrecord[self.s_count - 1] == 1):#return the character
			word = word + '.'
			#self.wordrecord[self.s_count - 1] = word
		elif(self.markrecord[self.s_count - 1] == 2):#return the character
			word = word + ','
			#self.wordrecord[self.s_count - 1] = word
		elif(self.markrecord[self.s_count - 1] == 3):#return the character
			word = word + '?'
			#self.wordrecord[self.s_count - 1] = word
		elif(self.markrecord[self.s_count - 1] == 4):#return the character
			word = word + '!'
			#self.wordrecord[self.s_count - 1] = word
		elif(self.markrecord[self.s_count - 1] == 5):#return the character
			word = word + '"'
			#self.wordrecord[self.s_count - 1] = word
		self.tbox.insertPlainText(word) #insert the result
		#if(i != self.s_count - 1): #not last one
		self.tbox.insertPlainText(" ") # add back space we had strip
		
		#self.clear()
			
		
	def clear(self):
		self.D = numpy.zeros((40, 40))
		#list
		self.D1 = []
		self.D2 = []
		self.D3 = []
		#count length
		self.D1C = 0
		self.D2C = 0
		self.D3C = 0

		self.word = 'Something'
		self.minDistance = 10000 #big enough when initial
		self.closestword = self.word
		self.equal = 0
		
	def do_action(self, spl):
		I = len(spl)
		linenum = 0
		for line in self.f:
			linenum+=1
			A = spl
			line = line.replace('\n','')
			B = line
			J = len(line)

			if(A[0] == B[0]):
				self.D[0][0] = 0
			else:
				self.D[0][0] = 1
			for i in range(1,I):
				self.D[i][0]=self.D[i-1][0] + 1
			for j in range(1,J):
				self.D[0][j]=self.D[0][j-1] + 1
			for i in range(1,I):
				for j in range(1,J):
					c1 = 0
					if(A[i] == B[j]):
						c1 = self.D[i-1][j-1] + 0
					else:
						c1 = self.D[i-1][j-1] + 1
					c2 = self.D[i-1][j] + 1
					c3 = self.D[i][j-1] + 1
					self.D[i,j] = min(c1, c2, c3)

			Distance = self.D[I-1,J-1]

			if(Distance == 1):
				self.D1.append(B)
				self.D1C += 1
			if(Distance == 0):
				self.closestword = B
				self.equal = 1
				break # if once eqaul we don't need to found rest
		
		self.pressed = 0
		#popup
		msgbox = QMessageBox()
		msgbox.setWindowTitle("Warning!")
		msgbox.setText("The Spelling of word: "+spl+" \nis Incorrect!\nChoose some choice:")
		
		
		#things to output
		R = []
		numtooutput = 0		
		if(self.equal == 1):
			self.pressed = 1
		else:
			for i in range(0,self.D1C):
				b = str(self.D1[i])
				msgbox.addButton(b, QMessageBox.ActionRole)
		nowword = 'Something'
		if(self.equal != 1):
			msgbox.exec_() #execute messagebox(will wait until response)
			nowword = str(msgbox.clickedButton().text()) #temp
			# msgbox.done(1)
		elif(self.equal == 1):
			nowword = spl
		
		#clear the result
		self.clear()
		
		self.f.seek(0) #back to the begining of dictionary
		
		return nowword
		
		
	def check_route(self, D, I, J, distance): #check route by backtrack
		dis = distance
		dis = D[I-1][J-1] # start by end
		a = 'No operation'
		b = 'Insertion'
		c = 'Substitution'
		d = 'Deletion'
		route = []
		i = I - 1
		j = J - 1
		run = 1 #detect whether to stop
		while run:
			#print('nn')
			if(i-1 >= 0 and j >= 0):
				d1 = D[i-1][j]
			else:
				d1 = 1000
			if(j-1 >= 0 and i >= 0):
				d2 = D[i][j-1]
			else:
				d2 = 1000
			if(i-1 >= 0 and j-1 >= 0):
				d3 = D[i-1][j-1]
			else:
				d3 = 1000
			if(((d1 == 1000) and (d2 == 1000)) and (d3 == 1000)):
				run = 0
				break
			else:
				m = min(d1, d2, d3)
			if(d3 == m): #Shortest route prior
				if(d3 == dis):
					route.insert(0,a) # use insert because backtrack; insert to front
				else:
					route.insert(0,c)
				#print(m, i, j)
				i = i - 1
				j = j - 1
				
			elif(d2 == m):
				route.insert(0,d)
				#print(m, i, j)
				j = j - 1
			else:
				route.insert(0,b)
				#print(m, i, j)
				i = i - 1
			dis = m
			
		if(D[0][0] == 0):
			route.insert(0, a)
		else:
			route.insert(0, c)
			
		return route
			

#main program call			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWind()
	sys.exit(app.exec_())