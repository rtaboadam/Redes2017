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
from cStringIO import StringIO
from numpy.lib import format
import cv2
class MyApiClient:
    """Clase que implementa el servidor en nuestro chat"""
    def __init__(self,my_ip='localhost',my_port=Puerto_5000):
        """
        Metodo contructor de la clase
        @param <string> my_ip: La dirección del ip
        @param <int> my_port: El puerto de mi servidor
        """
        puerto = str(my_port)
        uri = 'http://'+my_ip+':'+puerto
        self.proxy = xmlrpclib.ServerProxy(uri)
        self.grabadora = MyRecordAudio(formato=pyaudio.paInt16, channels=1,rate=44100,input1=True,frames_per_buffer=1024)
        self.llamando = False
        self.transmitiendo = False

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
        #self.proxy.stop()
    def no_video(self):
        self.transmitiendo = False
        self.proxy.stop()

    def toString(self,data):
        f= StringIO()
        format.write_array(f,data)
        return f.getvalue()

    def transmite(self):
        #self.cap = cv2.VideoCapture(0)
        self.transmitiendo = True
        #self.queue = mp.Queue()
        self.p1 = threading.Thread(target=self.grabaVideo)
        self.p1.daemon = True
        self.p1.start()
        #self.grabaVideo(self.queue)
        
    def grabaVideo(self):
        #self.transmitiendo = True
        cap = cv2.VideoCapture(0)
        while self.transmitiendo:
            ret, frame = cap.read()
            #cv2.imshow('Cliente',frame)
            #cv2.waitKey(5) 
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
            data = xmlrpclib.Binary(self.toString(frame))
            self.proxy.sendVideo_wrapper(data)
            print "enviando frame" 
        cap.release()

        cv2.destroyAllWindows()


        
