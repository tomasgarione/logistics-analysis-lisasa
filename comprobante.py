from pedido import Pedido
from estadopedido import EstadoPedido
from datetime import datetime
from excepciones import DatosInvalidosError, EstadoPedidoError
from validaciones import *

class Comprobante:

    def __init__(self, id_comprobante: str, pedido: Pedido, receptor: str, fecha_hora:datetime):
        validar_cadena_no_vacia(id_comprobante, "ID del comprobante", "Comprobante")
        validar_cadena_no_vacia(receptor, "Receptor del comprobante", "Comprobante")
        validar_datetime(fecha_hora, "Fecha y hora", "Comprobante")
        validar_instancia(pedido, Pedido, "Pedido", "Comprobante")
        self.id_comprobante = id_comprobante
        self.pedido = pedido
        self.receptor = receptor
        self.fecha_hora = fecha_hora

    @classmethod
    def generar(cls, pedido , receptor: str):
        if pedido.estado != EstadoPedido.EN_CAMINO:
            raise EstadoPedidoError(
                f"Solo se puede entregar un pedido EN_CAMINO. "
                f"Estado actual: {pedido.estado.value}."
            )
        
        comprobante = cls(
            id_comprobante=f"COMP-{pedido.id_pedido}",
            pedido=pedido,
            receptor=receptor,
            fecha_hora=datetime.now()    # registra el momento real
        )
        
        pedido.avanzar_estado()
        
        return comprobante

    def __str__(self):
        return f"Comprobante('{self.id_comprobante}', receptor='{self.receptor}', fecha='{self.fecha_hora.strftime('%d/%m/%Y %H:%M')}')"
    
    def __repr__(self):
        return f"Comprobante(id={self.id_comprobante!r}, pedido={self.pedido.id_pedido!r}, receptor={self.receptor!r})"