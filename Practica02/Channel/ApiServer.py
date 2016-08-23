#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../Constants/')
from Constants import *
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import Binary

def foo():
    return 'foo'
stack = None
class MyApiServer(threading.Thread):
    def __init__(self, my_port = Puerto_6000):
        """
        Metodo contructor de la clase
        @param <int> my_port: El puerto en el que va escuchar
        el servidor
        """
        super(MyApiServer,self).__init__()
        self.servidor = SimpleXMLRPCServer(('localhost',my_port)
                                           ,logRequests=True
                                           , allow_none=True)
        self.servidor.register_introspection_functions()
        self.servidor.register_multicall_functions()

        self.servidor.register_function(foo)
        self.servidor.register_instance(FunctionWrapper())

    def run(self):
        """
        Metodo que inicia el servidor que tiene como
        atributo
        """
        print "Servidor corriendo"
        print "Ctrl-c para salir"
        self.servidor.serve_forever()

    def verMensajes(self):
        """
        Metodo que regresa la lista de mensajes
        """
        return stack



class FunctionWrapper:
    def __init__(self):
        """
        Metodo contructor de la clase
        @param <list> stack: La pila de los mensajes
        """
        self.stack = stack = []
        
    def moo(self):
        return 'moo'
    
    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para mostrar el texto en nuestra pantalla.
    ************************************************** """
    def sendMessage_wrapper(self, message):
        self.stack = self.stack + [message]
        print message
        return message
    
    def getStack(self):
        """
        Metodo que regresa la lista de mensajes
        """
        return self.stack



if __name__ == '__main__':
    x = MyApiServer()
    x.run()
