from PyQt4 import QtGui
from ChatWindow import ChatWindow
# from mainwindow import Ui_MainWindow

class Login(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.textName.text() == 'foo' and
            self.textPass.text() == 'bar'):
            self.accept()
        else:
            QtGui.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    login = Login()
    login.hide()
    if login.exec_() == QtGui.QDialog.Accepted:
        login.hide()
        #sys.exit(app.exec_())
        window = ChatWindow()
        window.show()
        sys.exit(login.exec_())
        sys.exit(app.exec_())