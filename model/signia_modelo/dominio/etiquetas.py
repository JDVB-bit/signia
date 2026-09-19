"""🏷️ Forma canonica de una etiqueta: la que decide si dos muestras son la misma clase.

La etiqueta la escribe una persona al grabar, asi que llega con espacios y
mayusculas arbitrarias. Aqui se decide -en un solo sitio- que `" Hola "` y
`"hola"` son la misma sena y no dos clases del dataset.

No confundir con `infra.nombres_de_ruta.sanear`, que ademas quita todo lo que
no sea seguro en un nombre de carpeta: eso es una cuestion de disco, no de
dominio.
"""

from __future__ import annotations


def normalizar_etiqueta(texto: str) -> str:
    """Etiqueta en su forma canonica: sin espacios alrededor y en minusculas."""
    return texto.strip().lower()
