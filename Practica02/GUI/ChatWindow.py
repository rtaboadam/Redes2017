#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,'/')
#sys.path.append('../Constants/')
#from Constants import *
sys.path.append('../Channel/')
from Channel.Channel import *
from PyQt4 import QtGui

class ChatWindow(QtGui.QMainWindow):

	def __init__(self,parent=None,contact_ip=None,my_port=None,contact_port=None):
		super(ChatWindow, self).__init__(parent)
                self.channel = Channel(contact_ip,contact_port,my_port,self)
                self.initGUI(self.channel)
	
	def initGUI(self,channel):
		#self.channel = channel
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle("Chat")
		self.widget.resize(250,250)

		self.grid = QtGui.QGridLayout()
		self.widget.setLayout(self.grid)
		self.output_widget = QtGui.QTextEdit()
		self.output_widget.setReadOnly(True)
		self.input_widget = QtGui.QLineEdit()
		self.button_send = QtGui.QPushButton("Enviar")
		self.button_call = QtGui.QPushButton("Llamar")
		self.grid.addWidget(self.output_widget,0,0)
		self.grid.addWidget(self.input_widget,1,0)
		self.grid.addWidget(self.button_send,2,0)
		self.grid.addWidget(self.button_call,2,1)

		self.button_send.clicked.connect(lambda: self.enviar(str(self.input_widget.text())))
		self.button_call.clicked.connect(lambda: self.llamar())
		self.widget.show()
	
	def enviar(self, mensage):
		self.output_widget.append(mensage)
		self.input_widget.setText("")
		self.channel.send_text(mensage)

	def llamar(self):
		self.channel.send_audio()

def main():
	app = QtGui.QApplication(sys.argv)
	mainWindow = ChatWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
