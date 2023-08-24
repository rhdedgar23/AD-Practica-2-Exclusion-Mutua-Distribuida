#
# Implementa la simulacion del problema de Exclusion Mutua usando el modelo de Cliente-Servidor
#
# Elaboro: Edgar Daniel Rodriguez Herrera
#

import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation
import random
import time

class algoritmoExclusionMutua(Model):#se ejecuta por cada proceso/modelo que se asocia con cada nodo del grafo
  # Esta clase desciende de la clase Model e implementa los metodos
  # "init()" y "receive()", que en la clase madre se definen como abstractos

  def init(self):
      # Aqui se definen e inicializan los atributos particulares del algoritmo
      print("Inicio funciones", self.id)
      print("Mis vecinos son: ", end=" ")
      for neighbor in self.neighbors:
          # self.sucesor = neighbor
          print(neighbor, end=" ")
      print("\n")

      if self.id==1:#nodo 1, variable de estado solicitud libre (0) y la cola (de solicitudes) vacia
          self.estadoSeccionCritica= 0 # 0 -> libre, 1 -> ocupada
          self.colaSolicitudes= []



  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    if self.id != 1:# si es un nodo de la periferia
        if event.getName() == "INICIA":
            p= random.randint(1,4)
            if p==1:#la probabilidad de que salga cualquier valor de 1 a 4 es de 0.25
                print("[", self.id, "]: recibi INICIA en t=", self.clock, " \n", "Envio solicitud", "\n")
                newevent = Event("SOLICITUD", self.clock + random.randint(1, 4), self.neighbors, self.id, event.counter+1)
                # name, time, target, source, counter
                if newevent.getTime() <= maxtime:
                    self.transmit(newevent)
                else:
                    print("Mensajes intercambiados: ", event.counter)
            else:
                print("[", self.id, "]: recibi INICIA en t=", self.clock, " \n", "NO Envio solicitud", "\n")
        elif event.getName() == "OK":
            print("[", self.id, "]: Entro a la seccion critica en t=", self.clock, " \n")
            dormir= random.randint(1,5)
            time.sleep(dormir)
            print("[", self.id, "]: Salgo de la seccion critica en t=", self.clock+dormir, " \n")
            newevent = Event("LIBERA", self.clock + dormir, self.neighbors, self.id, event.counter+1)
            if newevent.getTime() <= maxtime:
                self.transmit(newevent)
            else:
                print("Mensajes intercambiados: ", event.counter)
    else:#si es el nodo 1
        if event.getName() == "SOLICITUD":
            #primero checa si la seccion critica esta disponible

        elif event.getName() == "LIBERA":
            print("")
    #en anillo, la variable de estado de solicitud se pone en verdadero




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

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = algoritmoExclusionMutua()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
# imprime el nodo escogido al azar para el evento semilla
for nodo in range(2, len(experiment.graph)+1):
    seed = Event("INICIA", 0.0, nodo, nodo, 0)#name, time, target, source, counter
    experiment.init(seed)
experiment.run()