from datetime import datetime, timedelta, time
from math import sqrt
from validaciones import *
from almacen import Almacen
from excepciones import DatosInvalidosError


class Ruta:
    def __init__(self, id_ruta, almacenes, velocidad_km_h=40.0):
       validar_cadena_no_vacia(id_ruta, "ID de la ruta", Ruta)
       if not isinstance(almacenes, list) or len(almacenes) < 2:
           raise DatosInvalidosError("La ruta debe definirse con al menos dos almacenes.")
       for almacen in almacenes:
           validar_instancia(almacen, Almacen, "Almacén", Ruta)
       validar_numero_positivo(velocidad_km_h, "Velocidad", Ruta)
       self.id_ruta = id_ruta
       self.almacenes = almacenes
       self.velocidad_km_h = velocidad_km_h

    def incluye_almacen(self, almacen_destino):
       return almacen_destino in self.almacenes
   
    def calcular_distancia_entre(self, origen, destino):
       dx = destino.x - origen.x
       dy = destino.y - origen.y
       return sqrt(dx*dx + dy*dy)

    def calcular_distancia_total(self):
       if len(self.almacenes) < 2:
           return 0.0
       distancia = 0.0
       for i in range(len(self.almacenes) - 1):
           distancia += self.calcular_distancia_entre(
               self.almacenes[i],
               self.almacenes[i + 1]
           )
       return distancia

    def estimar_tiempos(self, hora_salida: time):
       tiempos = {}
       ahora = datetime.combine(datetime.today(), hora_salida)

       for index in range(1, len(self.almacenes)):
           distancia = self.calcular_distancia_entre(
               self.almacenes[index - 1],
               self.almacenes[index]
           )
           minutos = round((distancia / self.velocidad_km_h) * 60)
           ahora += timedelta(minutes=minutos)
           tiempos[self.almacenes[index].id_almacen] = ahora.time()

       return tiempos

    def verificar_ventana(self, pedido, hora_salida_viaje: time):
       tiempos_estimados = self.estimar_tiempos(hora_salida_viaje)
       estimada = tiempos_estimados.get(pedido.destino.id_almacen)
       if estimada is None:
           return False

       return pedido.franja_inicio <= estimada <= pedido.franja_fin