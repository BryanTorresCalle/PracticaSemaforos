# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 22:23:15 2021

@author: carlo
"""


import threading as thread
from  time import sleep
from  time import time
import queue
import random
global t0
BUFFER_SIZE = 10
count = 0
queue = []
sen_reader = thread.Semaphore()
sen_area = thread.Semaphore()

class Process():

  def __init__(self, name):
    self.name = name


def Consumer(process):
    global t0
    global count
    while True:
        sen_reader.acquire()
        if not queue:
            print("Nada en la cola, consumidor esperando")
            sleep(random.random())
            print("El productor agrego algo a la cola, notificando al consumidor")
        if len(queue) != 0:
            num = queue.pop(0)
        print("Consumido", num)
        sen_reader.release()
        t1 = time() - t0
        print("Tiempo en que termina: %0.0fs" % (t1))
        sleep(random.random())      
      

def Producer(process):
    global t0
    nums = range(5)
    while True:
        sen_area.acquire()      
        if len(queue) == BUFFER_SIZE:
            print("Cola llena, el productor esta esperando")
            sleep(random.random())   
            print("Espacio en la cola, el consumidor notificara al productor")
        num = random.choices(nums)
        queue.append(num)
        print("Producido", num)
        sen_area.release()
        t1 = time() - t0
        print("Tiempo en que termina: %0.0fs" % (t1))
        sleep(random.random())       
def main():
    global t0
    t0 = time()
    thread.Thread(target = Consumer, args = ("Consumidor",)).start()
    thread.Thread(target = Producer, args = ("Productor",)).start()   

main()