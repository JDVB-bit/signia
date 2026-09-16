"""Genera los fixtures de conformidad JS <-> Python (Fase 0).

Cada fixture lleva una muestra cruda y el tensor que Python produce a partir de
ella. El test de JS (`front/app/src/lib/__tests__/`) leera estos mismos ficheros
y comprobara que su remuestreo coincide a 1e-5. Es la red que impide que el
navegador y el entrenamiento acaben viendo tensores distintos.

Uso:
    python scripts/generar_fixtures.py          # regenera tests/fixtures/

Reutiliza las fabricas de los tests a proposito: la mano canonica debe estar
definida en un unico sitio.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from signia_modelo.aplicacion.preprocess import construir_entrada  # noqa: E402
from signia_modelo.aplicacion.remuestreo import indices_remuestreo  # noqa: E402
from signia_modelo.dominio.contrato import T, VERSION_PREPROCESADO  # noqa: E402
from signia_modelo.dominio.entidades import Frame, Lado, MuestraAislada  # noqa: E402
from signia_modelo.infra.json_contrato import muestra_a_dict  # noqa: E402
from tests import factorias  # noqa: E402

CARPETA = RAIZ / "tests" / "fixtures"
DECIMALES = 6


def _muestra(frames, etiqueta: str) -> MuestraAislada:
    return MuestraAislada(
        frames=tuple(frames),
        sesion="2026-09-20-fixtures",
        fps_aprox=30.0,
        etiqueta=etiqueta,
    )


def casos() -> dict[str, MuestraAislada]:
    """Los casos limite que el remuestreo tiene que resolver igual en los dos lados."""
    der, izq = Lado.DERECHA, Lado.IZQUIERDA

    intermitente = []
    for t in range(35):
        if t < 8:
            lados = ()                 # la mano aun no ha entrado en el encuadre
        elif t < 18:
            lados = (der,)
        elif t < 22:
            lados = (izq,)             # cambio de mano
        else:
            lados = (izq, der)
        intermitente.append(factorias.frame(t, lados, desplazamiento=(0.3 + t / 100, 0.4)))

    return {
        "un_frame": _muestra([factorias.frame(0, (der,))], "hola"),
        "corta_12": _muestra(
            [factorias.frame(t, (der,), desplazamiento=(t / 20, 0.5)) for t in range(12)],
            "hola",
        ),
        "exacta_48": _muestra(
            [factorias.frame(t, (der,), escala=1 + t / 100) for t in range(T)], "como"
        ),
        "larga_120": _muestra(
            [
                factorias.frame(t, (izq, der), desplazamiento=(t / 200, 0.2))
                for t in range(120)
            ],
            "estar",
        ),
        "sin_manos": _muestra([Frame(t) for t in range(20)], "reposo"),
        "intermitente": _muestra(intermitente, "tu"),
    }


def fixture(nombre: str, muestra: MuestraAislada) -> dict:
    entrada = construir_entrada(muestra)
    return {
        "nombre": nombre,
        "version_preprocesado": VERSION_PREPROCESADO,
        "T": T,
        "muestra": muestra_a_dict(muestra),
        "esperado": {
            "indices": indices_remuestreo(muestra.n_frames, T),
            # Aplanados en orden C: (T, 2) y (T, 2, 21, 3).
            "presencia": [round(v, DECIMALES) for v in entrada.presencia.ravel().tolist()],
            "lm": [round(v, DECIMALES) for v in entrada.lm.ravel().tolist()],
        },
    }


def main() -> None:
    CARPETA.mkdir(parents=True, exist_ok=True)
    for nombre, muestra in casos().items():
        ruta = CARPETA / f"{nombre}.json"
        with ruta.open("w", encoding="utf-8") as fh:
            json.dump(fixture(nombre, muestra), fh, ensure_ascii=False)
        print(f"{ruta.relative_to(RAIZ)}  ({muestra.n_frames} frames)")


if __name__ == "__main__":
    main()
