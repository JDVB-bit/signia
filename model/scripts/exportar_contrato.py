"""Exporta las constantes del contrato a `model/contrato.json` (Fase 2).

Por que existe: la conformidad de la Fase 0 compara **tensores**. Eso detecta
una divergencia en el remuestreo, pero no una en las constantes: si alguien
cambia `SCHEMA`, `IDX_MUNECA` o `N_MANOS` en un solo lado, los fixtures siguen
pasando y el error aparece mucho despues, ya con dataset grabado.

Este script convierte `dominio/contrato.py` en un JSON que los dos lados leen:
pytest comprueba que el fichero en disco es el que produce el codigo actual, y
vitest comprueba que `front/app/src/dominio/contrato.js` declara los mismos
valores. Cambiar una constante en un solo lenguaje deja de compilar la suite.

Uso:
    python scripts/exportar_contrato.py          # regenera model/contrato.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from signia_modelo.dominio import contrato  # noqa: E402

#: Destino del export. Vive junto a `contrato.md`, su gemelo en prosa.
DESTINO = RAIZ / "contrato.json"

#: Nombre de constante publica: mayusculas, digitos y guion bajo.
_NOMBRE_DE_CONSTANTE = re.compile(r"^[A-Z][A-Z0-9_]*$")

#: Tipos que sobreviven al viaje por JSON sin perder informacion.
_TIPOS_EXPORTABLES = (bool, int, float, str, tuple)

#: Constantes que el front **tambien** tiene que declarar, con el por que.
#:
#: - `SCHEMA`: el front escribe el campo `schema` de cada muestra que exporta.
#: - `N_LANDMARKS`, `N_DIMS`, `N_MANOS`: forma del tensor que construye en JS.
#: - `IDX_MUNECA`: origen de la forma; el front lo usa al dibujar y al validar.
#: - `T`: longitud de la ventana; si difiere, el modelo recibe otro tensor.
#: - `SCORE_MAXIMO`: valor que asume cuando MediaPipe no reporta confianza.
#: - `LADOS_CANONICOS`: orden de las ranuras de mano, no el de deteccion.
#: - `TIPO_AISLADA`: tipo que el front pone en las muestras que graba.
CLAVES_COMPARTIDAS_CON_JS: tuple[str, ...] = (
    "SCHEMA",
    "N_LANDMARKS",
    "N_DIMS",
    "N_MANOS",
    "IDX_MUNECA",
    "T",
    "SCORE_MAXIMO",
    "LADOS_CANONICOS",
    "TIPO_AISLADA",
)

#: Aviso dentro del propio fichero: es generado, no se edita a mano.
GENERADO_POR = "model/scripts/exportar_contrato.py"

#: Sangria del JSON: legible en un diff, que es donde se va a revisar.
SANGRIA = 2


def _exportable(valor: Any) -> bool:
    """Descarta lo que no es una constante de datos (tipos, modulos, funciones)."""
    return isinstance(valor, _TIPOS_EXPORTABLES)


def _serializar(valor: Any) -> Any:
    """Tupla -> lista; el resto viaja tal cual."""
    return list(valor) if isinstance(valor, tuple) else valor


def constantes() -> dict[str, Any]:
    """Todas las constantes publicas de `contrato.py`, por descubrimiento.

    Se recorre el modulo en vez de enumerar los nombres a mano: asi una
    constante nueva entra en el export sin que nadie tenga que acordarse, y el
    test de sincronia la vigila desde el primer momento.
    """
    return {
        nombre: _serializar(valor)
        for nombre, valor in vars(contrato).items()
        if _NOMBRE_DE_CONSTANTE.match(nombre) and _exportable(valor)
    }


def contrato_exportado() -> dict[str, Any]:
    """El documento completo que se escribe en disco."""
    encontradas = constantes()
    faltantes = [clave for clave in CLAVES_COMPARTIDAS_CON_JS if clave not in encontradas]
    if faltantes:
        raise SystemExit(
            f"se declararon como compartidas constantes que ya no existen: {faltantes}"
        )
    return {
        "generado_por": GENERADO_POR,
        "version_preprocesado": contrato.VERSION_PREPROCESADO,
        "compartidas_con_js": list(CLAVES_COMPARTIDAS_CON_JS),
        "constantes": encontradas,
    }


def main() -> None:
    documento = contrato_exportado()
    with DESTINO.open("w", encoding="utf-8") as fichero:
        json.dump(documento, fichero, ensure_ascii=False, indent=SANGRIA)
        fichero.write("\n")
    print(f"{DESTINO.relative_to(RAIZ)}  ({len(documento['constantes'])} constantes)")


if __name__ == "__main__":
    main()
