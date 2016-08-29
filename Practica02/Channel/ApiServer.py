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



class FunctionWrapper:
    def __init__(self,interfaz):
        """
        Metodo contructor de la clase
        @param <list> stack: La pila de los mensajes
        """
        self.interfaz = interfaz
        self.stack = stack = []
        self.audio = []
        
    def moo(self):
        return 'moo'
    
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

    def sendAudio_wrapper(self,audioChunks):
        wf = wave.open(sys.argv[1], 'rb')
        p = pyaudio.PyAudio()
        audio = audioChunks.pila
        waveFile = wave.open("file.wav", 'wb')
        waveFile.setnchannels(2)
        waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(44100)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        stream = p.open(pyaudio.paInt16, 2,44100, True,1024)
        data = waveFile.readframes(1024)
        while len(data) > 0:
            stream.write(data)
            data = waveFile.readframes(1024)
        stream.close()    
        p.terminate()




if __name__ == '__main__':
    x = MyApiServer()
    x.run()
