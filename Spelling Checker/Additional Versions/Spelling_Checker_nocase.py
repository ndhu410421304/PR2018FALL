#Spelling Checker
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import numpy

class CheckResult():
	def __init__(self):
		#super().__init__()
		#self.init()
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

		self.word = 'Something'
		self.minDistance = 10000 #big enough when initial
		self.closestword = self.word
		self.equal = 0
		
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
		self.closestword = word
		self.equal = 0
		
	def do_action(self):
		I = len(self.word)
		linenum = 0
		route3 = []
		route2 = []
		route1 = []
		for line in self.f:
			linenum+=1
			A = self.word.lower() #lower the case when checking, but print original ones
			line = line.replace('\n','')
			B = line.lower()
			J = len(line) #because it include changeline character, so -1(old stuff)

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

			if(B == 'ac'):
				print(Distance)
			
			if(Distance == 3):
				self.D3.append(line) #append original word
				self.D3C += 1
				route3.append(str(self.check_route(self.D, I, J, 3)))
			if(Distance == 2):
				self.D2.append(line)
				self.D2C += 1
				route2.append(str(self.check_route(self.D, I, J, 1)))
			if(Distance == 1):
				self.D1.append(line)
				self.D1C += 1
				route1.append(str(self.check_route(self.D, I, J, 1)))
			if(Distance == 0):
				self.closestword = line
				self.equal = 1
				break # if once eqaul we don't need to found rest
		
		#things to output
		R = []
		numtooutput = 0		
		if(self.equal == 1):
			R.append('The spelling is correct!')
			numtooutput = 1
		else:
			R.append('Spelling is wrong.')
			R.append('Word with distance 1:')
			for i in range(0,self.D1C):
				
				R.append(self.D1[i] + " " + route1[i])
			R.append('Word with distance 2:')
			for i in range(0,self.D2C):
				R.append(self.D2[i] + " " + route2[i])
			R.append('Word with distance 3:')
			for i in range(0,self.D3C):
				R.append(self.D3[i] + " " + route3[i])
			numtooutput = 4 + self.D1C + self.D2C + self.D3C
		return R, numtooutput
		
		#clear the result
		self.clear()
		
	def check_route(self, D, I, J, distance): #check route by backtrack
		dis = distance
		dis = D[I-1][J-1] # start by end
		a = 'No Operation'
		b = 'Insertion'
		c = 'Substitution'
		d = 'Deletion'
		route = []
		i = I - 1
		j = J - 1
		run = 1 #detect whether to stop
		while run:
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
				i = i - 1
				j = j - 1
				
			elif(d2 == m):
				route.insert(0,d)
				j = j - 1
			else:
				route.insert(0,b)
				i = i - 1
			dis = m
			
		if(D[0][0] == 0):
			route.insert(0, a)
		else:
			route.insert(0, c)
			
		return route
		

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

	def initUI(self):
		self.setGeometry(0,0,500,500)
		grid = QGridLayout()
		
		self.msg = QLabel()
		self.msg.setText("Type in the word you want to check spelling.")
		self.msg.setAlignment(Qt.AlignLeft)
		grid.addWidget(self.msg, 0,1,0,2)
		
		self.lbox = QLineEdit()
		grid.addWidget(self.lbox, 1,1,1,2)
		
		Sbutton = QPushButton('Check')
		Sbutton.clicked.connect(self.press)
		Sbutton.setStyleSheet("QPushButton {font: bold; background-color: white;font-size: 24px;}") #initial button
		grid.addWidget(Sbutton, 2,1,2,2)
		
		self.tbox = QTextEdit()
		grid.addWidget(self.tbox, 4,1,4,2)
		
		self.setLayout(grid) #put them all in layout
		self.show()
		
	def press(self):
		#clear Textbox first
		self.tbox.clear()
		
		check = CheckResult()
		check.word = str(self.lbox.text()) #need to convert Qstirng to normal string!! (important)
		R, num = check.do_action()
		
		#progress bar
		progress = QProgressDialog(self)
		progress.setWindowTitle("Wait a bit...")
		progress.setLabelText("Checking...")
		progress.setCancelButtonText("Cancel Checking")
		progress.setWindowModality(Qt.WindowModal)
		
		progress.setRange(0,num)
		
		for n in range(0, num):
			self.tbox.setText(self.tbox.toPlainText() + R[n])
			self.tbox.setText(self.tbox.toPlainText() + '\n')
			
			#set progress bar
			progress.setValue(n)
			if progress.wasCanceled():
				QMessageBox.warning(self,"Warning","Checking Canceled")
				break #break when the checking had beend canceld by user
		else:
			progress.setValue(num)
			QMessageBox.information(self,"Done","Checking done")
			
			

#main program call			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWind()
	sys.exit(app.exec_())