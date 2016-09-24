#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../Constants/')
from Constants.Constants import *
import threading
import wave
import pyaudio
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import Binary
import numpy as np
import numpy
import cv
import cv2
CHUNK = 1024
CHANNELS = 1 
RATE = 44100
DELAY_SECONDS = 5

def foo():
    return 'foo'
stack = None
class MyApiServer(threading.Thread):
    def __init__(self, my_port = Puerto_6000,interfaz=None):
        """
        Metodo contructor de la clase
        @param <int> my_port: El puerto en el que va escuchar
        el servidor
        """
        super(MyApiServer,self).__init__()
        self.servidor = SimpleXMLRPCServer(('localhost',my_port)
                                           ,logRequests=True
                                           , allow_none=True)
        self.interfaz = interfaz
        self.servidor.register_introspection_functions()
        self.servidor.register_multicall_functions()

        self.servidor.register_function(foo)
        self.servidor.register_instance(FunctionWrapper(interfaz))
        self.widget = None

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
    def stop(self):
        self.servidor.shutdown()
        self.servidor.server_close()


class FunctionWrapper:
    def __init__(self,interfaz):
        """
        Metodo contructor de la clase
        @param <list> stack: La pila de los mensajes
        """
        self.interfaz = interfaz
        self.stack = stack = []
        self.audio = []
        self.frames = []
    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para mostrar el texto en nuestra pantalla.
    ************************************************** """
    def sendMessage_wrapper(self, message):
        self.stack = self.stack + [message]
        self.interfaz.output_widget.append(message)
        print message
        return message
    
    def getStack(self):
        """
        Metodo que regresa la lista de mensajes
        """
        return self.stack

    def sendAudio_wrapper(self,audio):
        p = pyaudio.PyAudio()
        FORMAT = p.get_format_from_width(2)
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)
        data = audio.data
        stream.write(data)
        stream.close()
        p.terminate()
        #playVThread = threading.Thread(target=sendAudio_wrapper, args=(,))
        #playVThread.setDaemon(True)
        #playVThread.start()
    def sendVideo_wrapper(self,video):
        #self.frames.append(toArray(video.data))
        while True:
            cv2.imshow('Servidor',toArray(video.data))
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
        cv2.destroyAllWindows()
    def reproduce():
        while True:
            if len(self.frames) > 0:
                cv2.imshow('Servidor',self.frames.pop(0))
                if cv2.waitKey(1) & 0xFF==ord('q'):
                    break
        cv2.destroyAllWindows()
    




if __name__ == '__main__':
    x = MyApiServer()
    x.run()
