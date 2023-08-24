#
# Implementa la simulacion de un TRIS/TRAS
#
# Elaboro: Edgar Daniel Rodriguez Herrera
#

import sys
import Star
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation
import random

class AlgoritmoTrisTras(Model):#se ejecuta por cada proceso/modelo que se asocia con cada nodo del grafo
  # Esta clase desciende de la clase Model e implementa los metodos
  # "init()" y "receive()", que en la clase madre se definen como abstractos

  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo
    print ("Inicio funciones", self.id)
    print("Mis vecinos son: ", end=" ")
    for neighbor in self.neighbors:
        #self.sucesor = neighbor
        print(neighbor, end=" ")
    #print("\n")

    if self.id != 1:#solo los nodos diferentes de 1 pueden tomar la decision
        decision= random.randint(0,1)#0 -> no, 1 -> si
        if decision == 1:
            decisiones.append(self.id)#se agrega el nodo a la lista de decisiones
        print("\nDecision tris: ", decision, "\n")
    else:
        print("\n")


  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento

    if event.getName() == "INICIA":#si es el evento semilla
       print ("[", self.id, "]: recibi INICIA en t=",self.clock, "\n")
       # name, time, target, source, counter
       newevent = Event("TRIS", self.clock + random.randint(1,4), self.neighbors[0], self.id, event.counter+1)
       if newevent.getTime() <= maxtime:
           self.transmit(newevent)
       else:
           print("Mensajes intercambiados: ", event.counter)
    elif event.getName() == "TRIS":#si el nodo 1 recibe un tris
       fuente= event.source
       print("[", self.id, "]: recibi peticion TRIS de [", fuente, "] en t=", self.clock)
       print("Recursos disponibles: ", Star.recursos, "\n")
       Star.peticiones += 1

       if Star.recursos > 0:#si tiene recursos disponibles
           newevent = Event("TRAS", self.clock + random.randint(1,4), fuente, self.id, event.counter+1)
           Star.recursos -= 1
           if newevent.getTime() <= maxtime:
               self.transmit(newevent)
           else:
               print("Mensajes intercambiados: ", event.counter)
               exit(0)
       else:#si NO tiene recursos disponibles
           newevent = Event("TRUS", self.clock + random.randint(1, 4), fuente, self.id, event.counter + 1)
           if newevent.getTime() <= maxtime:
               self.transmit(newevent)
           else:
               print("Mensajes intercambiados: ", event.counter)
               exit(0)
    elif event.getName() == "TRAS":#se consumio un recurso y se salta al proximo nodo
        print("[", self.id, "]: recibi TRAS de [", event.source, "] en t=", self.clock)
        if len(decisiones)>0 and len(decisiones)!=1:
            decisiones.pop(0)#quitamos el primer nodo (ya atendido) de la lista
            print("Decisiones tris restantes: ", decisiones, "\n")
            newevent = Event("TRIS", self.clock + random.randint(1, 4), event.source, decisiones[0], event.counter + 1)
            if newevent.getTime() <= maxtime:
                self.transmit(newevent)
            else:
                print("Mensajes intercambiados: ", event.counter)
        else:#si se atendio el ultimo nodo de la lista
            decisiones.pop(0)
            print("Ya no existen peticiones TRIS")
            print("Peticiones TRIS atendidas: ", Star.peticiones)
            print("Recursos restantes: ", Star.recursos)
            exit(0)
    elif event.getName() == "TRUS":#ya no hay recursos
        print("[", self.id, "]: recibi TRUS de [", event.source, "] en t=", self.clock)
        print("Ya NO existen recursos!")
        exit(1)
# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------
# construye una instancia de la clase Simulation recibiendo como parametros el nombre del
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
   print ("Por favor proporcione el nombre de la grafica de comunicaciones")
   raise SystemExit(1)

maxtime= 60
# se crea un contador de recursos disponibles para el nodo 1
recursos= random.randint(1, 5)
peticiones= 0
# se crea una lista en donde se van guardando las decisiones de peticion tris
decisiones= []

experiment = Simulation(sys.argv[1], maxtime)#filename, maxtime

# imprime lista de nodos que se extraen del archivo
# experiment.graph[indice+1 == nodo] == vecino
print("Lista de nodos: ", experiment.graph)

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = AlgoritmoTrisTras()
    experiment.setModel(m, i)

# imprime la lista de decisiones
print("Decisiones tris: ", decisiones, "\n")
# de esta lista se elige al primer nodo para que sea el evento semilla
# inserta un evento semilla en la agenda y arranca
if len(decisiones)!=0:#si hay almenos 1 elemento con peticion TRIS
    seed = Event("INICIA", 0.0, decisiones[0], decisiones[0], 0)
    #name, time, target, source, counter
    experiment.init(seed)
    experiment.run()
else:
    print("No hay peticiones TRIS!")
    exit(1)