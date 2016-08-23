#! /usr/bin/env python
# -*- coding: utf-8 -*-
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

class MyApiClient:
    """Clase que implementa el servidor en nuestro chat"""
    def __init__(self,my_ip='localhost',my_port=5000):
        """
        Metodo contructor de la clase
        @param <string> my_ip: La dirección del ip
        @param <int> my_port: El puerto de mi servidor
        """
        puerto = str(my_port)
        uri = 'http://'+my_ip+':'+str(puerto)
        self.proxy = xmlrpclib.ServerProxy(uri)


    def sendMessage(self,text):
        """
        Metodo que envia un mesaje
        @param <string> text: El texto a enviar
        """
        return self.proxy.sendMessage_wrapper(text)
        
