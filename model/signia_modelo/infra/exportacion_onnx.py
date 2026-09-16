"""📦 Exportacion de un modulo de torch a un grafo ONNX con ejes dinamicos.

Vive en infra porque depende de dos frameworks. Ejecutar el grafo exportado es
otra responsabilidad y vive en `ejecucion_onnx.py`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import torch
from torch import nn
from torch.export import Dim

#: Version del conjunto de operadores ONNX (soportada por onnxruntime-web).
OPSET_ONNX = 17

#: Posicion de los ejes dinamicos en cada tensor de entrada.
EJE_LOTE = 0
EJE_TIEMPO = 1


def exportar(
    modulo: nn.Module,
    ejemplo: Sequence[torch.Tensor],
    ruta: Path | str,
    *,
    nombres_entrada: Sequence[str],
    nombre_salida: str,
    opset: int = OPSET_ONNX,
) -> Path:
    """Exporta `modulo` a ONNX con el lote y el tiempo como ejes dinamicos.

    Los dos ejes se comparten entre todas las entradas: el grafo exige que `lm`
    y `presencia` tengan el mismo lote y la misma duracion, que es justo el
    invariante del contrato.
    """
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    # 🔗 Las mismas instancias de Dim en todas las entradas = ejes compartidos
    lote = Dim("lote")
    tiempo = Dim("tiempo")
    ejes = tuple({EJE_LOTE: lote, EJE_TIEMPO: tiempo} for _ in ejemplo)

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
