import pytest
from datetime import time
from paquete import Paquete
from cliente import Cliente
from almacen import Almacen
from pedido import Pedido
from motocicleta import Motocicleta
from furgoneta import Furgoneta
from camion import Camion
from mensajeroexterno import MensajeroExterno
from ruta import Ruta
from viaje import Viaje

@pytest.fixture
def almacen_a():
    return Almacen("ALM-01", "Central", "Av. Corrientes 1234", 0.0, 0.0)

@pytest.fixture
def almacen_b():
    return Almacen("ALM-02", "Norte", "Av. Santa Fe 2000", 3.0, 4.0)

@pytest.fixture
def cliente_base():
    return Cliente("Juan Perez", "Calle Falsa 123", "30111222", "1122334455", "juan@mail.com")

@pytest.fixture
def paquete_liviano():
    return Paquete("PKG-01", peso=5.0, volumen=0.1, descripcion="Sobre")

@pytest.fixture
def paquete_pesado():
    return Paquete("PKG-02", peso=90.0, volumen=0.4, descripcion="Caja grande")

@pytest.fixture
def pedido_base(cliente_base, almacen_b):
    return Pedido("PED-001", cliente_base, almacen_b, time(9, 0), time(18, 0))

@pytest.fixture
def moto():
    return Motocicleta("MOTO-001", "Honda Titan")

@pytest.fixture
def furgoneta():
    return Furgoneta("FURG-001", "Renault Kangoo")

@pytest.fixture
def camion():
    return Camion("CAMI-001", "Mercedes Benz")

@pytest.fixture
def mensajero():
    return MensajeroExterno("MENS-001", "Rappi Express")

@pytest.fixture
def ruta_ab(almacen_a, almacen_b):
    return Ruta("RUTA-01", [almacen_a, almacen_b], velocidad_km_h=40.0)

@pytest.fixture
def viaje_furgoneta(furgoneta, almacen_a, ruta_ab):
    return Viaje("VJ-001", furgoneta, almacen_a, ruta_ab, hora_salida=time(8, 53))