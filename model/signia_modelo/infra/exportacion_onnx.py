"""Exportacion a ONNX y comprobacion de paridad torch <-> onnxruntime.

Vive en infra porque depende de dos frameworks. Lo usan el test de la Fase 0 y
`exportar_onnx.py` de la Fase 4: la comprobacion de paridad **no es opcional**,
es donde aparecen los bugs de exportacion.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import torch
from torch import nn
from torch.export import Dim


def exportar(
    modulo: nn.Module,
    ejemplo: Sequence[torch.Tensor],
    ruta: Path | str,
    *,
    nombres_entrada: Sequence[str],
    nombre_salida: str,
    opset: int = 17,
) -> Path:
    """Exporta `modulo` a ONNX con el lote y el tiempo como ejes dinamicos.

    Los dos ejes se comparten entre todas las entradas: el grafo exige que `lm`
    y `presencia` tengan el mismo lote y la misma duracion, que es justo el
    invariante del contrato.
    """
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    lote = Dim("lote")
    tiempo = Dim("tiempo")
    ejes = tuple({0: lote, 1: tiempo} for _ in ejemplo)

    modulo.eval()
    with torch.no_grad():
        torch.onnx.export(
            modulo,
            tuple(ejemplo),
            str(ruta),
            input_names=list(nombres_entrada),
            output_names=[nombre_salida],
            dynamic_shapes=ejes,
            opset_version=opset,
            dynamo=True,
        )
    return ruta


def salida_onnx(
    ruta: Path | str,
    entradas: dict[str, np.ndarray],
) -> np.ndarray:
    """Ejecuta el grafo con onnxruntime (lo mismo que hara el navegador)."""
    import onnxruntime as ort

    sesion = ort.InferenceSession(str(ruta), providers=["CPUExecutionProvider"])
    return sesion.run(None, entradas)[0]
