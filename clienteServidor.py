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
          self.contador=0
          self.estadoSeccionCritica= 0 # 0 -> libre, 1 -> ocupada
          self.colaSolicitudes= []

  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    if self.id != 1:# si es un nodo de la periferia
        if event.getName() == "INICIA":
            p= random.randint(1,4)
            if p==1:#la probabilidad de que salga cualquier valor de 1 a 4 es de 0.25
                print("[", self.id, "]: recibi INICIA en t=", self.clock, "\n", "Envio solicitud", "\n")
                newevent = Event("SOLICITUD", self.clock+1, self.neighbors[0], self.id)
                if newevent.getTime() <= maxtime:
                    self.transmit(newevent)
                else:
                    print("Tiempo maximo agotado!")
            else:
                print("[", self.id, "]: recibi INICIA en t=", self.clock, " \n", "NO Envio solicitud", "\n")
        elif event.getName() == "OK":
            print("[", self.id, "]: recibi OK en t=", self.clock, "\n")
            print("[", self.id, "]: Entro a la seccion critica en t=", self.clock, " \n")
            dormir= random.randint(1,5)
            time.sleep(dormir)
            print("[", self.id, "]: Salgo de la seccion critica en t=", self.clock+dormir, " \n")
            newevent = Event("LIBERA", self.clock + dormir, self.neighbors[0], self.id)
            if newevent.getTime() <= maxtime:
                self.transmit(newevent)
            else:
                print("Tiempo maximo agotado!")
    else:#si es el nodo 1
        if event.getName() == "SOLICITUD":
            print("[", self.id, "]: recibi SOLICITUD  de [", event.source, "] en t=", event.time)
            self.contador += 1
            #primero checa si la seccion critica esta disponible
            #si esta disponible,
            if self.estadoSeccionCritica==0:
                print("Seccion Critica disponible!", "\n")
                #pone el estado de la seccion critica en ocupado (==1)
                self.estadoSeccionCritica=1
                #y luego mando OK a P_j
                self.contador += 1
                newevent = Event("OK", event.time+1, event.source, self.id)
                self.transmit(newevent)
            #si no esta disponible
            else:
                #encola a P_j en Q
                self.colaSolicitudes.append(event.source)

        elif event.getName() == "LIBERA":
            print("[", self.id, "]: recibi LIBERA  de [", event.source, "] en t=", event.time)
            self.contador += 1
            #si la cola de solicitudes esta vacia
            if len(self.colaSolicitudes)==0:
                #ponemos el estado de la seccion critica como libre (==0)
                self.estadoSeccionCritica=0
                print("Ya no hay mas solicitudes!", "\n", "Total de mensajes transmitidos: ", self.contador, "\n")
            #si no esta vacia (tiene solicitantes)
            else:
                #enviamos OK al primer solicitante de la cola
                self.contador += 1
                newevent = Event("OK", event.time+1, self.colaSolicitudes[0], self.id)
                self.transmit(newevent)
                #y eliminamos a este solicitante de la cola
                self.colaSolicitudes.pop(0)
    #en anillo, la variable de estado de solicitud se pone en verdadero
# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------
# construye una instancia de la clase Simulation recibiendo como parametros el nombre del
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
   print ("Por favor proporcione el nombre de la grafica de comunicaciones")
   raise SystemExit(1)

maxtime= 60
experiment = Simulation(sys.argv[1], maxtime)#filename, maxtime

# imprime lista de nodos que se extraen del archivo
# experiment.graph[indice+1 == nodo] == vecino
print("Lista de nodos: ", experiment.graph)

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = algoritmoExclusionMutua()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
for nodo in range(2, len(experiment.graph)+1):
    seed = Event("INICIA", nodo-2, nodo, nodo)#name, time, target, source
    experiment.init(seed)
experiment.run()