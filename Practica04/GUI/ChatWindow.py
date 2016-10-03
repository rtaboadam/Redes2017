#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,'/')
#sys.path.append('../Constants/')
#from Constants import *
sys.path.append('../Channel/')
from Channel.Channel import *
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *
import threading

class ChatWindow(QtGui.QMainWindow):

	def __init__(self,parent=None,contact_ip=None,my_port=5000,contact_port=5000):
		super(ChatWindow, self).__init__(parent)
                self.channel = Channel(contact_ip,contact_port,my_port,self)
                self.initGUI(self.channel)
        print contact_ip
	
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
		self.button_stop = QtGui.QPushButton("Colgar")
		self.button_video= QtGui.QPushButton("Video")
		self.grid.addWidget(self.output_widget,0,0)
		self.grid.addWidget(self.input_widget,1,0)
		self.grid.addWidget(self.button_send,2,0)
		self.grid.addWidget(self.button_stop,2,2)
                #Boton de llamada
		self.grid.addWidget(self.button_call,2,1)
		self.grid.addWidget(self.button_video,3,0)

		self.button_send.clicked.connect(lambda: self.enviar(str(self.input_widget.text())))
		self.button_call.clicked.connect(lambda: self.llamar())
		self.button_stop.clicked.connect(lambda: self.stopCall())
		self.button_video.clicked.connect(lambda: self.transmitir())
		self.widget.show()
		self.popup = None
		#self.btnExit.clicked.connect(self.close)
		#self.actionExit.triggered.connect(self.close)

	def close_event(self, event):
		reply = QtGui.QMessageBox.question(self, 'Message',"Deseas cerrar el chat?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			self.channel.server.stop()
			event.accept()
		else:
			event.ignore()
	
	def enviar(self, mensage):
		self.output_widget.append(mensage)
		self.input_widget.setText("")
		self.channel.send_text(mensage)
	def stopCall(self):
		self.channel.stop_audio()
		self.channel.stop_video()

	def llamar(self):
		#self.popup = MyPopup(self)
		#self.popup.exec_()
		#self.channel.send_audio()
		self.channel.send_audio()
	def transmitir(self):
		self.channel.send_video()
		
class MyPopup(QtGui.QDialog):
	def __init__(self,widget,parent = None):
		QWidget.__init__(self)
		self.initUI(widget)
	def close_event(self, event):
		reply = QtGui.QMessageBox.question(self, 'Message',"Deseas cerrar el chat?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			self.channel.server.stop()
			event.accept()
		else:
			event.ignore()
	def exec__(widget=None):
		widget.channel.client.grabadora.graba()

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.fillRect(event.rect(), QtGui.QColor(99, 0, 0))
	def initUI(self,widget):
		self.label1 = QtGui.QLabel('Llamando...',self)
		self.buttonAceptar = QtGui.QPushButton('Colgar', self)
		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(self.label1)
		layout.addWidget(self.buttonAceptar)
		self.buttonAceptar.clicked.connect(lambda: self.close_audio(widget))
		#self.connect(self.buttonAceptar, QtCore.SIGNAL('clicked()'), self.close_audio(widget))
		self.setWindowTitle("Llamado")
		self.show()
	def run(self):
		self.show()
	def stop(self):
		return 0
	def close_audio(self,widget):
		widget.channel.client.grabadora.parametro = False
		self.close()
	def main():
		app = QtGui.QApplication(sys.argv)
		mainWindow = ChatWindow()
		mainWindow.show()
		sys.exit(app.exec_())
	if __name__ == '__main__':
		main()
