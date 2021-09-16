
import threading as thread
from  time import sleep
from  time import time
import queue
global count
global t0
count = 0

#global x                #Shared Data
#global sen_reader
#global sen_area

sen_reader = thread.Semaphore()
sen_area = thread.Semaphore()

class Process():

  def __init__(self, name, time, type_process):
    self.name = name
    self.time = time
    self.type_process = type_process

def Reader(process):
  
    global count
    
    sen_reader.acquire()
    count += 1
    if count == 1: sen_area.acquire()
    
    sen_reader.release()
    
    #Consultar Area
    
    sleep(process.time)
    t1 = time() - t0
    print("Ejecutando Proceso: ", process.name)
    print("Tiempo en que termina: %0.0fs" % (t1))
    sen_reader.acquire()
    count -= 1
    if count == 0: sen_area.release()
    
    sen_reader.release()
    sleep(process.time)      
      

def Writer(process):
  
    
    sen_area.acquire()      
    #Consultar Area
    
    sleep(process.time)
    t1 = time() - t0
    print("Ejecutando Proceso: ", process.name)
    print("Tiempo en que termina: %0.0fs" % (t1))
    sen_area.release()     
    sleep(process.time)      




def main():
  queue_process = queue.Queue()
  while True: 
    name = input("Ingrese el nombre del proceso: ")
    time_e = int(input("Ingrese el tiempo de ejecucion: "))
    type_process = input("Ingrese R si es un lector, W si es un escritor: ")
    if name is not None and time_e is not None and type_process is not None:
      queue_process.put(Process(name, time_e, type_process))
      flag = input("Escriba 1 para seguir agregando, o pulse cualquier tecla para terminar de agregar procesos: ")
      if flag != "1": break
  
  global t0
  t0 = time()
  
  while queue_process.empty() == False:
      
      p = None
      current_process = queue_process.get()
      if str(current_process.type_process) == "R":
          p = thread.Thread(target = Reader, args = (current_process,))
      
      elif str(current_process.type_process) == "W":
          p = thread.Thread(target = Writer, args = (current_process,))    
        
      p.start()
      
    
    

main()
