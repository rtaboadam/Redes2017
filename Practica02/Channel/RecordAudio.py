import pyaudio
import wave
import threading

class MyRecordAudio(threading.Thread):	
	def __init__(self, format=pyaudio.paInt16, channels=2,rate=44100, input=True,frames_per_buffer=1024):
		super(MyRecordAudio,self).__init__()
		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(pyaudio.paInt16, 2,44100, True,1024)
		self.parametro = True

	def graba(self):
		self.frames = []
		self.pila = []

		while self.parametro is True:
			pila.append(self.stream.read(1024))
			frames.append(pila[-1])
		print "grabacion realizada"

	def run(self):
		print "grabando"
		self.graba()

	def modificaParametro(self):
		self.parametro = not parametro



