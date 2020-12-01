from threading import Thread
import time
class UnpackThreadClass (Thread):
   def __init__(self, name):
      Thread.__init__(self)
      self.name = name
   def run(self):
      print("Thread '" + self.name + "' avviato")      
      print("Thread '" + self.name + "' terminato")