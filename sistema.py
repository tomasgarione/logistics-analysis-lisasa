from collections import deque
from excepciones import CapacidadExcedidaError, VentanaHorariaError, EstadoViajeError, DatosInvalidosError
from viaje import Viaje
 
 
class Sistema:
    def __init__(self):
        self.transportes = []
        self.almacenes   = []
        self.pedidos: deque = deque()
        self.viajes  = []
        self.pedidos_no_asignados: deque = deque()
 
    def cargar_almacen(self, almacen):
        self.almacenes.append(almacen)
 
    def cargar_transporte(self, transporte):
        self.transportes.append(transporte)
 
    def cargar_pedido(self, pedido):
        #append() encola al final, el primero en entrar será el primero en salir 
        self.pedidos.append(pedido)
 
    def cargar_nuevo_viaje(self, transporte, almacen, ruta, hora_salida):
        id_viaje = f"Viaje-{len(self.viajes) + 1}"
        nuevo_viaje = Viaje(id_viaje, transporte, almacen, ruta, hora_salida)
        self.viajes.append(nuevo_viaje)
        return nuevo_viaje
 
    def reintentar_pedidos_no_asignados(self):
        while self.pedidos_no_asignados:
            self.pedidos.append(self.pedidos_no_asignados.popleft())
 
    def procesar_siguiente_pedido(self):
        if not self.pedidos:
            return None
        #popleft() desencola el primero que entró, O(1) con deque 
        pedido_actual = self.pedidos.popleft()
        resultado = {
            "pedido_id": pedido_actual.id_pedido,
            "destino_nombre": pedido_actual.destino.nombre,
            "urgente": pedido_actual.urgente,
            "eventos": []
        }
        viajes_compatibles = [
            viaje for viaje in self.viajes
            if viaje.ruta.incluye_almacen(pedido_actual.destino)
        ]
        if not viajes_compatibles:
            resultado["eventos"].append(("sin_viajes", pedido_actual.id_pedido))
            #append() encola al final de la cola de no-asignados
            self.pedidos_no_asignados.append(pedido_actual)
            return resultado
        asignado = False
        for viaje in viajes_compatibles:
            try:
                viaje.agregar_pedido(pedido_actual)
                pedido_actual.avanzar_estado()   #PENDIENTE → EN_CAMINO
                resultado["eventos"].append((
                    "asignado",
                    viaje.id_viaje,
                    viaje.transporte.__class__.__name__,
                    viaje.transporte.patente,
                    pedido_actual.estado.value
                ))
                asignado = True
                break
            except EstadoViajeError:
                resultado["eventos"].append(("rechazo_estado_viaje", viaje.id_viaje))
            except CapacidadExcedidaError:
                resultado["eventos"].append(("rechazo_capacidad", viaje.id_viaje))
            except VentanaHorariaError:
                resultado["eventos"].append(("rechazo_ventana", viaje.id_viaje))
            except DatosInvalidosError:
                resultado["eventos"].append(("rechazo_incompatibilidad", viaje.id_viaje))
        if not asignado:
            resultado["eventos"].append(("no_asignado", pedido_actual.id_pedido))
            self.pedidos_no_asignados.append(pedido_actual)
        return resultado