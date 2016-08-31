import pyaudio
import wave
import numpy
import multiprocessing as mp
#import threading

class MyRecordAudio():	
	def __init__(self, formato=pyaudio.paInt16, channels=2,rate=44100
                     , input1=True,frames_per_buffer=1024):

 #               super(MyRecordAudio,self).__init__()
		self.format=formato
		self.channels=channels
		self.rate=rate
		self.input=input1
		self.frames_per_buffer=frames_per_buffer
		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(format=self.format
                                              , channels=self.channels
                                              ,rate = self.rate
                                              , input = self.input
                                              ,frames_per_buffer = self.frames_per_buffer)
		self.parametro = True

	def graba(self,q):
		self.q = q
		self.frames = []
		self.pila = []
		while True:
			self.pila.append(self.stream.read(1024))
			self.frames.append(self.pila[-1])
		data_ar = numpy.fromstring(''.join(pila),  dtype=numpy.uint8)
		self.q.put(data_ar)

	def run(self):
		print "grabando"
		self.graba()

	def modificaParametro(self):
		self.parametro = not parametro



