#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../Constants/')
from Constants.Constants import *
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from RecordAudio import MyRecordAudio
import pyaudio
import multiprocessing as mp
import threading
class MyApiClient:
    """Clase que implementa el servidor en nuestro chat"""
    def __init__(self,my_ip='localhost',my_port=Puerto_5000):
        """
        Metodo contructor de la clase
        @param <string> my_ip: La dirección del ip
        @param <int> my_port: El puerto de mi servidor
        """
        puerto = str(my_port)
        uri = 'http://'+my_ip+':'+str(puerto)
        self.proxy = xmlrpclib.ServerProxy(uri)
        self.grabadora = MyRecordAudio(formato=pyaudio.paInt16, channels=1,rate=44100,input1=True,frames_per_buffer=1024)
        self.llamando = False

    def stopAudio(self):
        self.llamando = False

    def sendMessage(self,text):
        """
        Metodo que envia un mesaje
        @param <string> text: El texto a enviar
        """
        return self.proxy.sendMessage_wrapper(text)

    def sendAudio(self):
        #self.grabadora = MyRecordAudio(formato=pyaudio.paInt16, channels=2,rate=44100,input1=True,frames_per_buffer=1024)
        self.queue = mp.Queue()
        self.p = threading.Thread(target=self.grabadora.graba, args=(self.queue,))
        self.p.daemon = True
        self.p.start()
        self.llamando = True  
        while self.llamando:
            d = self.queue.get()
            data = xmlrpclib.Binary(d)
            self.proxy.sendAudio_wrapper(data)
    def colgar(self):
        self.llamando = False
        self.proxy.stop()
        
