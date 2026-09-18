"""Mete en el dataset los lotes que descarga el boton *Enviar* del front.

Es el puente entre grabar y entrenar mientras el backend no este delante: el
front produce **un fichero con varias muestras** y el dataset guarda **una
muestra por fichero**. El endpoint `POST /muestras` hara exactamente esto
mismo, porque los dos llaman al mismo caso de uso.

Uso:
    python scripts/importar_lote.py descargas/signia-hola-2026-09-20-local.json
    python scripts/importar_lote.py descargas/*.json --datos D:/signia-data
    python scripts/importar_lote.py lote.json --seco     # valida sin escribir

Codigo de salida: 0 si entro todo, 1 si algun fichero era invalido. Ningun
fichero invalido deja el dataset a medias: se validan **todos** antes de
escribir **ninguno**.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from signia_modelo.aplicacion.importacion_de_lote import importar_lote  # noqa: E402
from signia_modelo.dominio.entidades import Muestra  # noqa: E402
from signia_modelo.dominio.errores import ErrorDeContrato  # noqa: E402
from signia_modelo.infra.ficheros_json import CODIFICACION  # noqa: E402
from signia_modelo.infra.json_lote import muestras_desde_lote  # noqa: E402
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco  # noqa: E402

#: Codigos de salida del proceso.
SALIDA_OK = 0
SALIDA_CON_ERRORES = 1


def argumentos() -> argparse.Namespace:
    """Opciones de linea de comandos."""
    analizador = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    analizador.add_argument("ficheros", nargs="+", help="lotes .json descargados del front")
    analizador.add_argument(
        "--datos",
        help="raiz del dataset (por defecto, la variable DATOS_DIR o ./data)",
    )
    analizador.add_argument(
        "--seco",
        action="store_true",
        help="valida y cuenta, pero no escribe nada en el dataset",
    )
    return analizador.parse_args()


def leer_lote(ruta: Path) -> list[Muestra]:
    """Lee un fichero de lote y devuelve sus muestras ya validadas."""
    with ruta.open(encoding=CODIFICACION) as fichero:
        try:
            datos = json.load(fichero)
        except json.JSONDecodeError as exc:
            raise ErrorDeContrato(f"JSON invalido ({exc})") from exc
    return muestras_desde_lote(datos)


def leer_todos(rutas: list[Path]) -> tuple[list[Muestra], list[str]]:
    """Valida todos los ficheros antes de tocar el dataset.

    Importar a medias es peor que no importar: dejaria el dataset en un estado
    que nadie recuerda, y las muestras que si entraron habria que buscarlas.
    """
    muestras: list[Muestra] = []
    errores: list[str] = []
    for ruta in rutas:
        try:
            del_fichero = leer_lote(ruta)
        except (ErrorDeContrato, OSError) as exc:
            errores.append(f"{ruta.name}: {exc}")
            continue
        print(f"  {ruta.name}: {len(del_fichero)} muestras")
        muestras.extend(del_fichero)
    return muestras, errores


def main() -> int:
    opciones = argumentos()
    rutas = [Path(fichero) for fichero in opciones.ficheros]
    repo = RepositorioMuestrasEnDisco(opciones.datos)

    print(f"Leyendo {len(rutas)} fichero(s):")
    muestras, errores = leer_todos(rutas)

    for error in errores:
        print(f"  ERROR {error}", file=sys.stderr)
    if errores:
        print("No se importo nada: corrige los ficheros invalidos.", file=sys.stderr)
        return SALIDA_CON_ERRORES

    if opciones.seco:
        print(f"\nEn seco: {len(muestras)} muestras validas, no se escribio nada.")
        return SALIDA_OK

    resultado = importar_lote(muestras, repo)
    print(f"\nImportadas {resultado.n_muestras} muestras en {repo.raiz.resolve()}")
    for etiqueta, cuantas in resultado.por_etiqueta.items():
        print(f"  {etiqueta}: +{cuantas}")
    print("\nSiguiente paso: python scripts/inspeccionar.py")
    return SALIDA_OK


if __name__ == "__main__":
    sys.exit(main())
