#
# Implementa la simulacion del problema de Exclusion Mutua usando el modelo de anillo
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

      #Variables de estado
      #por el valor de los nodos en el grafo 2 (no estan ordenados de menor a mayor o viceversa),
      #decimos que el sucesor del nodo j es el nodo que se inserto por ultimo en su lista de vecinos,
      #eso sirve ya que asi se formateo la representacion textual del grafo:
      #[vecino por detras] [vecino por delante]
      #en este caso el sentido del anillo es unidireccional en el sentido de las manecillas del reloj
      self.sucesor = self.neighbors[1]
      self.solicitud_sc = 0 #0->falso(no hay solicitud), 1->verdadero(existe solicitud circulante)

  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se recibe un evento
    if event.getName() == "INICIA":
        p = random.randint(1, 4)
        #la probabilidad de que salga cualquier valor de 1 a 4 es de 0.25
        if p == 1:
            print("[", self.id, "]: recibi INICIA en t=", self.clock, "\n")
            print("Genero el TOKEN!", "\n")
            token = Event("TOKEN", self.clock + 1, self.sucesor, self.id)
            print("Envio solicitud", "\n")
            solicitud = Event("SOLICITUD", self.clock + 1, self.id, self.id)
            if token.getTime() <= maxtime:
                self.transmit(token)
                self.transmit(solicitud)
            else:
                print("Tiempo maximo agotado!")
        else:
            print("[", self.id, "]: recibi INICIA en t=", self.clock, "\n")
            print("Genero el TOKEN!", "\n")
            token = Event("TOKEN", self.clock + 1, self.sucesor, self.id)
            print("NO envio solicitud", "\n")
            if token.getTime() <= maxtime:
                self.transmit(token)
            else:
                print("Tiempo maximo agotado!")
    elif event.getName() == "SOLICITUD":
        #cuando el algoritmo recibe una solicitud,
        print("[Algoritmo]: recibi SOLICITUD de [", event.source, "] en t=", event.time, "\n")
        #marca solicitud_sc como verdadera
        self.solicitud_sc = 1

    elif event.getName() == "TOKEN":
        print("[", self.id, "]: Recibi TOKEN de [", event.source, "] en t=", event.time, " \n")
        # si el nodo que recibe el token no tiene solicitud de acceso a la SC
        if self.solicitud_sc == 0:
            #decide si quiere mandar una solicitud
            p = random.randint(1, 4)
            #si decide el nodo enviar solicitud de acceso
            if p == 1:
                #envia solicitud al algoritmo
                print("Envio solicitud", "\n")
                solicitud = Event("SOLICITUD", self.clock + 1, self.id, self.id)
                self.transmit(solicitud)
                #y envia el token al sucesor
                token = Event("TOKEN", self.clock + 1, self.sucesor, self.id)
                if token.getTime() <= maxtime:
                    self.transmit(token)
                else:
                    print("Tiempo maximo agotado!")
            else:
                # si decide no enviar solicitud
                # envia el token al sucesor
                print("NO envio solicitud", "\n")
                token = Event("TOKEN", self.clock + 1, self.sucesor, self.id)
                if token.getTime() <= maxtime:
                    self.transmit(token)
                else:
                    print("Tiempo maximo agotado!")
        # si SI tiene una solicitud pendiente
        else:
            #el algoritmo envia OK a la app
            okay = Event("OK", self.clock + 1, self.id, self.id)
            self.transmit(okay)
    elif event.getName() == "OK":
        print("[", self.id, "]: Recibi OK del Algoritmo en t=", self.clock, " \n")
        print("[", self.id, "]: Entro a la seccion critica en t=", self.clock, " \n")
        dormir = random.randint(1, 5)
        time.sleep(dormir)
        print("[", self.id, "]: Salgo de la seccion critica en t=", self.clock + dormir, " \n")
        libera = Event("LIBERA", self.clock + dormir, self.id, self.id)
        self.transmit(libera)
    elif event.getName() == "LIBERA":
        print("[Algoritmo]: recibi LIBERA de [", event.source, "] en t=", event.time)
        self.solicitud_sc = 0
        token = Event("TOKEN", self.clock + 1, self.sucesor, self.id)
        if token.getTime() <= maxtime:
            self.transmit(token)
        else:
            print("Tiempo maximo agotado!")
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
seed = Event("INICIA", 0, 1, 1)#name, time, target, source
experiment.init(seed)
experiment.run()
