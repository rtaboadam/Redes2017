import sys

from PyQt4 import QtGui, QtCore
from PyQt4 import Qt

from ChatWindow import *

class Login1(QtGui.QWidget):
    def __init__(self):
        super(Login1,self).__init__()
        self.initUI()

    def initUI(self):
        self.label1 = QtGui.QLabel('Cual es mi puerto?',self)
        self.line1 = QtGui.QLineEdit(self)
        self.label2 = QtGui.QLabel('Cual es el puerto del contacto?',self)
        self.line2 = QtGui.QLineEdit(self)
        self.buttonAceptar = QtGui.QPushButton('Aceptar', self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.line1)
        layout.addWidget(self.label2)
        layout.addWidget(self.line2)
        layout.addWidget(self.buttonAceptar)
        self.connect(self.buttonAceptar, QtCore.SIGNAL('clicked()'), self.access_chat)
        self.setWindowTitle("Login")
        self.show()

    def access_chat(self):
        self.chat = ChatWindow(contact_ip ='localhost'
                               ,contact_port = int(self.line2.text())
                               ,my_port = int(self.line1.text()))
        self.close()

class Login2(QtGui.QWidget):
    def __init__(self):
        super(Login2,self).__init__()
        self.initUI()

    def initUI(self):
        self.label1 = QtGui.QLabel('Cual es mi ip?',self)
        self.line1 = QtGui.QLineEdit(self)
        self.label2 = QtGui.QLabel('Cual es la ip del contacto?',self)
        self.line2 = QtGui.QLineEdit(self)
        self.buttonAceptar = QtGui.QPushButton('Aceptar', self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.line1)
        layout.addWidget(self.label2)
        layout.addWidget(self.line2)
        layout.addWidget(self.buttonAceptar)
        self.connect(self.buttonAceptar, QtCore.SIGNAL('clicked()'), self.access_chat)
        self.setWindowTitle("Login")

    def access_chat(self):
        self.close()


def main():
    app = QtGui.QApplication(sys.argv)
    main = Login1()
    main.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
