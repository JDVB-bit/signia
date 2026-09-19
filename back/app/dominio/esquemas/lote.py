"""📦 Lo que llega a `POST /muestras`: el sobre, y solo el sobre.

Decision de diseno importante: **Pydantic no describe aqui el contrato de
datos**. Valida que venga un sobre con su `schema` y una lista de objetos, y
nada mas. Quien valida cada muestra es `signia_modelo.infra.json_lote`, que es
el mismo codigo que usa el importador de consola y el que se testea contra las
fixtures compartidas con el front.

Si el contrato se escribiera tambien en modelos Pydantic, habria dos
definiciones de "que es una muestra" que podrian separarse en silencio —
exactamente lo que el test de contrato cruzado existe para impedir.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

#: Al menos una muestra: un lote vacio es un error del cliente, no un exito.
MINIMO_DE_MUESTRAS = 1


class LoteEntrante(BaseModel):
    """El cuerpo de `POST /muestras`, identico al fichero que descarga el front."""

    schema_: int = Field(alias="schema", description="Version del formato del lote")
    muestras: list[dict[str, Any]] = Field(
        min_length=MINIMO_DE_MUESTRAS,
        description="Muestras crudas; las valida el paquete del modelo",
    )

    def como_dict(self) -> dict[str, Any]:
        """Vuelve al dict original para dárselo al validador del contrato."""
        return {"schema": self.schema_, "muestras": self.muestras}
