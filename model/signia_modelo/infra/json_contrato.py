"""🔄 Conversion entre el dict JSON del contrato y las entidades del dominio.

El JSON es el formato de transporte (front -> backend) y de almacenamiento. Es
la frontera del sistema: **todo lo que entra se valida aqui**, y a partir de
este punto el resto del codigo trabaja con entidades ya validas. Leer o
escribir ficheros NO es cosa de este modulo (ver `ficheros_json.py`).

Formato (schema 1), ver `model/contrato.md`:

    {
      "schema": 1,
      "tipo": "aislada" | "frase",        (opcional; por defecto "aislada")
      "etiqueta": "hola",                 (aisladas)
      "etiquetas": ["hola", "como"],      (frases)
      "sesion": "2026-09-20-snt-01",
      "fps_aprox": 30,
      "frames": [{"t": 0, "manos": [{"lado": "derecha", "score": 0.98,
                                     "lm": [[x, y, z], ...21]}]}]
    }
"""

from __future__ import annotations

from typing import Any, Mapping

from ..dominio.contrato import SCHEMA, SCORE_MAXIMO, TIPO_AISLADA, TIPO_FRASE
from ..dominio.entidades import Frame, Lado, Mano, Muestra, MuestraAislada, MuestraFrase
from ..dominio.errores import ErrorDeContrato

#: Si el cliente no envia `score`, se asume confianza plena (compatibilidad).
SCORE_POR_DEFECTO = SCORE_MAXIMO


def _exigir(condicion: bool, mensaje: str) -> None:
    """Lanza `ErrorDeContrato` con `mensaje` si la condicion no se cumple."""
    if not condicion:
        raise ErrorDeContrato(mensaje)


def _mano_desde_dict(datos: Any, contexto: str) -> Mano:
    """Dict de una mano -> `Mano`, anadiendo al error DONDE ocurrio."""
    _exigir(isinstance(datos, Mapping), f"{contexto}: una mano debe ser un objeto")
    _exigir("lado" in datos, f"{contexto}: falta 'lado'")
    _exigir("lm" in datos, f"{contexto}: falta 'lm'")
    landmarks = datos["lm"]
    _exigir(isinstance(landmarks, list), f"{contexto}: 'lm' debe ser una lista")
    try:
        return Mano(
            lado=Lado.desde_texto(str(datos["lado"])),
            score=float(datos.get("score", SCORE_POR_DEFECTO)),
            lm=tuple(tuple(punto) for punto in landmarks),
        )
    except ErrorDeContrato as exc:
        # La entidad ya sabe QUE esta mal; aqui se anade DONDE
        raise ErrorDeContrato(f"{contexto}: {exc}") from exc
    except (TypeError, ValueError) as exc:
        raise ErrorDeContrato(f"{contexto}: landmarks invalidos ({exc})") from exc


def _frame_desde_dict(datos: Any, indice: int) -> Frame:
    """Dict de un frame -> `Frame`; `t` toma el indice si no viene."""
    contexto = f"frame {indice}"
    _exigir(isinstance(datos, Mapping), f"{contexto}: debe ser un objeto")
    manos = datos.get("manos", [])
    _exigir(isinstance(manos, list), f"{contexto}: 'manos' debe ser una lista")
    try:
        t = int(datos.get("t", indice))
    except (TypeError, ValueError) as exc:
        raise ErrorDeContrato(f"{contexto}: 't' invalido") from exc
    return Frame(
        t=t,
        manos=tuple(
            _mano_desde_dict(mano, f"{contexto}, mano {posicion}")
            for posicion, mano in enumerate(manos)
        ),
    )


def muestra_desde_dict(datos: Any) -> Muestra:
    """Valida un dict del contrato y lo convierte en entidad.

    Lanza `ErrorDeContrato` con un mensaje accionable ante cualquier
    desviacion. Nunca devuelve una entidad a medias.
    """
    _exigir(isinstance(datos, Mapping), "la muestra debe ser un objeto JSON")
    schema = datos.get("schema")
    _exigir(schema == SCHEMA, f"schema {schema!r} no soportado (esperado {SCHEMA})")

    frames_json = datos.get("frames")
    _exigir(isinstance(frames_json, list), "falta la lista 'frames'")
    frames = tuple(_frame_desde_dict(frame, indice) for indice, frame in enumerate(frames_json))

    comunes: dict[str, Any] = {
        "frames": frames,
        "sesion": str(datos.get("sesion", "")),
        "fps_aprox": float(datos["fps_aprox"]) if datos.get("fps_aprox") is not None else None,
        "schema": SCHEMA,
    }

    # 🔀 El tipo decide que subclase construir; por defecto, aislada
    tipo = str(datos.get("tipo", TIPO_AISLADA))
    if tipo == TIPO_AISLADA:
        _exigir("etiqueta" in datos, "una muestra aislada necesita 'etiqueta'")
        return MuestraAislada(**comunes, etiqueta=str(datos["etiqueta"]))
    if tipo == TIPO_FRASE:
        etiquetas = datos.get("etiquetas")
        _exigir(isinstance(etiquetas, list), "una frase necesita 'etiquetas' (lista)")
        return MuestraFrase(**comunes, etiquetas=tuple(str(etiqueta) for etiqueta in etiquetas))
    raise ErrorDeContrato(
        f"tipo de muestra desconocido: {tipo!r} (validos: {TIPO_AISLADA}, {TIPO_FRASE})"
    )


def muestra_a_dict(muestra: Muestra) -> dict[str, Any]:
    """Entidad -> dict del contrato. Inverso exacto de `muestra_desde_dict`."""
    datos: dict[str, Any] = {
        "schema": muestra.schema,
        "tipo": muestra.tipo,
        "sesion": muestra.sesion,
        "fps_aprox": muestra.fps_aprox,
        "frames": [
            {
                "t": frame.t,
                "manos": [
                    {"lado": mano.lado.value, "score": mano.score, "lm": [list(p) for p in mano.lm]}
                    for mano in frame.manos
                ],
            }
            for frame in muestra.frames
        ],
    }
    if isinstance(muestra, MuestraAislada):
        datos["etiqueta"] = muestra.etiqueta
    else:
        datos["etiquetas"] = list(muestra.glosas)
    return datos
