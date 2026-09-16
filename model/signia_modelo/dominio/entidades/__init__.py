"""🧩 Entidades del dominio: lo que es una muestra, un frame y una mano.

Python puro e inmutable. Cada entidad vive en su propio modulo y se valida a si
misma al construirse: si existe una instancia, cumple el contrato. Aqui solo se
reexportan para que el resto del paquete importe desde un unico sitio.
"""

from .frame import Frame
from .lado import Lado
from .mano import Mano, Punto
from .muestra import Muestra
from .muestra_aislada import MuestraAislada
from .muestra_frase import MuestraFrase

__all__ = ["Frame", "Lado", "Mano", "Muestra", "MuestraAislada", "MuestraFrase", "Punto"]
