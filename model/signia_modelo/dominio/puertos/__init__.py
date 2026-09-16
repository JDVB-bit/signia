"""🔌 Puertos (interfaces) del dominio.

Son `Protocol`: quien los implementa no hereda de nada y el dominio no depende
de ninguna implementacion concreta (DIP). Cada puerto vive en su modulo y se
mantiene pequeno (ISP): quien solo lee muestras no arrastra la firma de guardar.
"""

from .remuestreador import Remuestreador
from .repositorio_muestras import EscritorMuestras, LectorMuestras, RepositorioMuestras

__all__ = ["EscritorMuestras", "LectorMuestras", "Remuestreador", "RepositorioMuestras"]
