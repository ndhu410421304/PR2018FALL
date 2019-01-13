#Test GUI
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

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
		#self.msg.setAlignment(Qt.AlignCenter)
		self.msg.setAlignment(Qt.AlignLeft)
		grid.addWidget(self.msg, 0,1,0,2)
		
		self.lbox = QLineEdit()
		#self.lbox.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
		#self.lbox.setAlignment(Qt.AlignCenter)
		grid.addWidget(self.lbox, 1,1,1,2)
		
		Sbutton = QPushButton('Check')
		Sbutton.clicked.connect(self.press)
		#Sbutton.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum) #setup size policy
		Sbutton.setStyleSheet("QPushButton {font: bold; background-color: white;font-size: 24px;}") #initial button
		grid.addWidget(Sbutton, 2,1,2,2)
		
		#self.msg = QMessageBox()
		#self.msg.setText("Test")
		#grid.addWidget(self.msg, 2,1,2,2)
		
		self.tbox = QTextEdit()
		#self.tbox.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
		#self.tbox.setAlignment(Qt.AlignCenter)
		grid.addWidget(self.tbox, 4,1,4,2)
		
		self.setLayout(grid) #put them all in layout
		self.show()
		
	def press(self):
		sender = self.sender()
		if sender.text() in ['Check']:
			self.tbox.setText(self.tbox.toPlainText() + 'check')
			self.tbox.setText(self.tbox.toPlainText() + '\n')
		
#main program call			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWind()
	sys.exit(app.exec_())