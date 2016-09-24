import pyaudio
import wave
import numpy
import multiprocessing as mp
#import threading

class MyRecordAudio():	
	def __init__(self, formato=pyaudio.paInt16, channels=1,rate=44100
                     , input1=True,frames_per_buffer=1024):

 #               super(MyRecordAudio,self).__init__()
		self.audio = pyaudio.PyAudio()
		self.format = self.audio.get_format_from_width(2)
		self.channels=channels
		self.rate=rate
		self.input=input1
		self.frames_per_buffer=frames_per_buffer
		self.stream = self.audio.open(format=self.format
                                              , channels=self.channels
                                              ,rate = self.rate
                                              , input = self.input
                                              ,frames_per_buffer = self.frames_per_buffer)

	def graba(self,q):
		self.frames = []
		self.pila = []
		while True:
			frame = []
			for i in range(0,int(44100/1024 *2)):
				frame.append(self.stream.read(1024))
			data_ar = numpy.fromstring(''.join(frame),  dtype=numpy.uint8)
			q.put(data_ar)

	def run(self):
		print "grabando"
		self.graba()

	def modificaParametro(self):
		self.parametro = not parametro



