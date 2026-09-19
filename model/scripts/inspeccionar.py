"""Informe del dataset crudo: ¿ya se puede entrenar? (Fase 2 del plan).

Contesta con numeros las tres preguntas que deciden si la fase esta hecha:
cuantas muestras hay por clase, si `reposo` esta sobrerrepresentada y si hay
frases suficientes para medir WER. Todo lo que no cumple sale como aviso.

Ademas dibuja la trayectoria de la muneca de una muestra concreta: los
promedios no distinguen una sena de una mano quieta, y el trazo si.

Uso:
    python scripts/inspeccionar.py
    python scripts/inspeccionar.py --datos D:/signia-data
    python scripts/inspeccionar.py --etiqueta hola
    python scripts/inspeccionar.py --trayectoria hola --muestra 3

Codigo de salida: 0 si el dataset cumple los criterios de la Fase 2, 1 si
queda algun aviso bloqueante. Asi el mismo comando sirve de puerta en un CI.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from signia_modelo.aplicacion.inspeccion import (  # noqa: E402
    REVISIONES,
    REVISIONES_DE_CADA_MUESTRA,
    diagnosticar,
    hay_bloqueos,
    resumir,
    trayectoria_de_muneca,
)
from signia_modelo.dominio.contrato import TIPO_AISLADA  # noqa: E402
from signia_modelo.dominio.entidades import Lado  # noqa: E402
from signia_modelo.dominio.errores import ErrorDeContrato  # noqa: E402
from signia_modelo.infra.ficheros_json import cargar_muestra  # noqa: E402
from signia_modelo.infra.informe_de_dataset import NOTA_VISTA_FILTRADA, informe  # noqa: E402
from signia_modelo.infra.lienzo_ascii import dibujar, leyenda  # noqa: E402
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco  # noqa: E402

#: Codigos de salida del proceso.
SALIDA_OK = 0
SALIDA_CON_BLOQUEOS = 1

#: Primera muestra de una clase, en el orden alfabetico de sus ficheros.
PRIMERA_MUESTRA = 1


def argumentos() -> argparse.Namespace:
    """Opciones de linea de comandos."""
    analizador = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    analizador.add_argument(
        "--datos",
        help="raiz del dataset (por defecto, la variable DATOS_DIR o ./data)",
    )
    analizador.add_argument(
        "--etiqueta",
        help="limita el informe a una sena (el diagnostico global deja de aplicar)",
    )
    analizador.add_argument(
        "--trayectoria",
        metavar="ETIQUETA",
        help="dibuja el recorrido de la muneca de una muestra de esa sena",
    )
    analizador.add_argument(
        "--muestra",
        type=int,
        default=PRIMERA_MUESTRA,
        help=f"cual dibujar, en orden alfabetico de fichero (por defecto {PRIMERA_MUESTRA})",
    )
    analizador.add_argument(
        "--lado",
        choices=[lado.value for lado in Lado],
        help="mano a dibujar (por defecto, la que aparece en mas frames)",
    )
    return analizador.parse_args()


def encabezado_del_informe(repo: RepositorioMuestrasEnDisco, etiqueta: str | None) -> str:
    """Primera linea del informe: de donde salen los datos."""
    filtro = f" (filtrado por '{etiqueta}')" if etiqueta else ""
    return f"Dataset SignIA en {repo.raiz.resolve()}{filtro}"


def imprimir_informe(repo: RepositorioMuestrasEnDisco, etiqueta: str | None) -> bool:
    """Imprime el informe y dice si hay avisos bloqueantes.

    Con `--etiqueta` el dataset que se ve es parcial, asi que los criterios
    globales se desactivan: decir "falta reposo" mirando solo 'hola' seria un
    falso bloqueo.
    """
    resumen = resumir(repo.listar(etiqueta=etiqueta) if etiqueta else repo.listar())
    avisos = diagnosticar(
        resumen, revisiones=REVISIONES_DE_CADA_MUESTRA if etiqueta else REVISIONES
    )
    lineas = informe(
        resumen,
        avisos,
        encabezado=encabezado_del_informe(repo, etiqueta),
        nota=NOTA_VISTA_FILTRADA if etiqueta else None,
    )
    for linea in lineas:
        print(linea)
    return hay_bloqueos(avisos)


def imprimir_trayectoria(
    repo: RepositorioMuestrasEnDisco,
    etiqueta: str,
    posicion: int,
    lado: str | None,
) -> None:
    """Dibuja el recorrido de la muneca de una muestra concreta."""
    rutas = repo.rutas(tipo=TIPO_AISLADA, etiqueta=etiqueta)
    if not rutas:
        raise SystemExit(f"no hay muestras de '{etiqueta}' en {repo.raiz.resolve()}")
    if not PRIMERA_MUESTRA <= posicion <= len(rutas):
        raise SystemExit(f"'{etiqueta}' tiene {len(rutas)} muestras; se pidio la {posicion}")

    ruta = rutas[posicion - 1]
    muestra = cargar_muestra(ruta)
    trazo = trayectoria_de_muneca(muestra, Lado(lado) if lado else None)

    print("")
    print(f"Trayectoria de la muneca {trazo.lado.value} en {ruta.name}")
    print(f"{muestra.n_frames} frames, mano presente en {len(trazo.presentes)}. {leyenda()}")
    if trazo.esta_vacia:
        print("(esa mano no aparece en ningun frame de la muestra)")
        return
    for linea in dibujar(trazo.puntos):
        print(linea)


def main() -> int:
    opciones = argumentos()
    repo = RepositorioMuestrasEnDisco(opciones.datos)

    try:
        bloqueado = imprimir_informe(repo, opciones.etiqueta)
        if opciones.trayectoria:
            imprimir_trayectoria(repo, opciones.trayectoria, opciones.muestra, opciones.lado)
    except ErrorDeContrato as error:
        # Una muestra corrupta en disco: decir cual y parar, no seguir contando
        raise SystemExit(f"dataset invalido: {error}") from error

    return SALIDA_CON_BLOQUEOS if bloqueado else SALIDA_OK


if __name__ == "__main__":
    sys.exit(main())
