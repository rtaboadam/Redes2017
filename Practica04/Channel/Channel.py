#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../Constants/')
from Constants.Constants import *
import xmlrpclib
from ApiServer import MyApiServer
from ApiClient import MyApiClient

from threading import Thread
"""**************************************************
Las instancias de esta clase contendran los metodos
necesarios para hacer uso de los metodos
del api de un contacto. Internamente Trabajara
con una proxy apuntando hacia los servicios del
servidor xmlrpc del contacto
**************************************************"""
class Channel:
    """**************************************************
        Constructor de la clase
        @param <str> contact_ip: Si no se trabaja de manera local
                    representa la ip del contacto con el que se
                    establecera la conexion
        @param <int> my_port: De trabajar de manera local puerto
                    de la instancia del cliente
        @param <int> contact_port: De trabajar de manera local
                    representa el puerto de la instancia del contacto
        **************************************************"""
    def __init__(self, contact_ip = "localhost", contact_port = Puerto_6000, my_port = Puerto_5000,interfaz=None):
        #TODO
        self.interfaz = interfaz
        self.client = MyApiClient(contact_ip,contact_port) 
        self.server = MyApiServer(my_port,self.interfaz)
        self.server.start()

    """**************************************************
    Metodo que se encarga de mandar texto al contacto con
    el cual se estableció la conexion
    **************************************************"""
    def send_text(self, text):
        #TODO
        return self.client.sendMessage(text)

    def send_audio(self):
        self.thread = Thread(target=self.client.sendAudio)  
        self.thread.daemon = True
        self.thread.start()

    def stop_audio(self):
        return self.client.colgar()
    def stop_video(self):
        return self.client.no_video()
    def send_video(self):
        #self.thread = Thread(target=self.client.transmite)  
        #self.thread.daemon = True
        #self.thread.start()
        self.client.transmite()


