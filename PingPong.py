# 
# Implementa la simulacion de un PING/PONG
#
# Elaboro: Elizabeth Perez Cortes
#

import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation
import random

class AlgorithmPingPong(Model):#se ejecuta por cada proceso/modelo que se asocia con cada nodo del grafo
  # Esta clase desciende de la clase Model e implementa los metodos 
  # "init()" y "receive()", que en la clase madre se definen como abstractos

  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo
    print ("Inicio funciones", self.id)
    self.sucesor = self.neighbors[0]
    print ("Mi vecino es:", self.sucesor)

  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento

    if event.getName() == "INICIA":#si es el evento semilla
       print ("[", self.id, "]: recibi INICIA en t=",self.clock," \n")
       newevent = Event("PING", self.clock + random.randint(1,4), self.sucesor, self.id, event.counter+1)
       #name, time, target, source, counter
       if newevent.getTime() <= maxtime:
        self.transmit(newevent)
       else:
        print("Mensajes intercambiados: ", event.counter)

    elif  event.getName() == "PING":#si se recibe un ping
       print ("[", self.id, "]: recibi PING en t=",self.clock," \n")
       newevent = Event("PONG", self.clock + random.randint(1,4), self.sucesor, self.id, event.counter+1)
       if newevent.getTime() <= maxtime:
           self.transmit(newevent)
       else:
           print("Mensajes intercambiados: ", event.counter)

    else:#si se recibe un pong
       print ("[", self.id, "]: recibi PONG en t=",self.clock," \n")
       newevent = Event("PING", self.clock + random.randint(1,4), self.sucesor, self.id, event.counter+1)
       if newevent.getTime() <= maxtime:
           self.transmit(newevent)
       else:
           print("Mensajes transmitidos: ", event.counter)

# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------
# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
   print ("Por favor proporcione el nombre de la grafica de comunicaciones")
   raise SystemExit(1)

maxtime= 20
experiment = Simulation(sys.argv[1], maxtime)#filename, maxtime

# imprime lista de nodos que se extraen del archivo
# experiment.graph[indice+1 == nodo] == vecino
print("Lista de nodos: ", experiment.graph)
# de esta lista de nodos se elige un nodo al azar y se guarda en nodoSeed para efectuar el evento semilla con el
nodoSeed= random.randint(1, len(experiment.graph))

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = AlgorithmPingPong()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
# imprime el nodo escogido al azar para el evento semilla
print("El nodo escogido aleatoriamente para el evento semilla es: ", nodoSeed)
seed = Event("INICIA", 0.0, nodoSeed, nodoSeed, 0)#name, time, target, source, counter
experiment.init(seed)
experiment.run()


