#! /usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
# PURPOSE:Interfaz grafica de un cliente en PyQt4    #
#                                                    #
# Vilchis Dominguez Miguel Alonso                    #
#       <mvilchis@ciencias.unam.mx>                  #
#                                                    #
# Notes: El alumno tiene que implementar la parte    #
#       comentada como TODO(Instalar python-qt)      #
#                                                    #
# Copyright   16-08-2015                             #
#                                                    #
# Distributed under terms of the MIT license.        #
#################################################### #
import sys, getopt
sys.path.insert(0,'/')
sys.path.append('./GUI')
sys.path.append('./Channel')
sys.path.append('./Constants')

from Login import *
from ChatWindow import *
from Constants import *
from Channel import *


# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "l", ["local="])
    except getopt.GetoptError:
        #TODO lanzar exepcion
        raise Exception("jajaj que creees no jala xD xD") 
    if opts: #Si el usuario mandó alguna bandera
        local = True if '-l' in opts[0] else False
    else:
        local = False
    app = QtGui.QApplication(sys.argv)
    if local:
        loginWindow = Login2()
    else:
        loginWindow = Login1()
    #TODO Llamar a su ventana de login
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
