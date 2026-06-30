import csv
from functools import reduce
from problema import TipoProblema
from transporte import Transporte
 
class AnalizadorOperaciones:
    PORCENTAJE_INFLACION = 0.15
    TIPO_CRITICOS = (TipoProblema.DANO,)
 
    def __init__(self, pedidos=None, transportes=None):
        self.pedidos = pedidos or []
        self.transportes = transportes or []
 
    def filtrar_incidencias_graves(self):
        todas = reduce(lambda acc, pedido: acc + pedido.incidencias, self.pedidos, [])
        graves = list(filter(lambda inc: inc.tipo in self.TIPO_CRITICOS, todas))
        descripciones = list(map(lambda inc: inc.descripcion, graves))
        return descripciones
 
    def ajustar_costos_por_inflacion(self):
        transportes_propios = filter(
            lambda t: isinstance(t, Transporte),
            self.transportes
        )
        return list(map(
            lambda t: ((1 + self.PORCENTAJE_INFLACION) * t.costo_base_km),
            transportes_propios
        ))
 
    def exportar_incidencias_csv(self, ruta="Incidencias_graves.csv"):
        descripciones = self.filtrar_incidencias_graves()
        if not descripciones:
            return None
        with open(ruta, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["descripcion"])
            writer.writerows(map(lambda d: [d], descripciones))
        return ruta

        
    
