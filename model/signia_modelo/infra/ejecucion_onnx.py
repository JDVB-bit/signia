"""▶️ Ejecucion de un grafo ONNX con onnxruntime, igual que lo hara el navegador.

Es la otra mitad de la comprobacion de paridad torch <-> ONNX, que **no es
opcional**: ahi es donde aparecen los bugs de exportacion.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

#: Se ejecuta en CPU para que el resultado no dependa de la GPU del equipo.
PROVEEDORES = ["CPUExecutionProvider"]


def salida_onnx(ruta: Path | str, entradas: dict[str, np.ndarray]) -> np.ndarray:
    """Ejecuta el grafo de `ruta` y devuelve su primera salida."""
    # Import diferido: quien solo exporta no necesita onnxruntime instalado
    import onnxruntime as ort

    sesion = ort.InferenceSession(str(ruta), providers=PROVEEDORES)
    return sesion.run(None, entradas)[0]
