"""Adaptador entre el JSON del contrato y las entidades del dominio.

El JSON es el formato de transporte (front -> backend) y de almacenamiento. Es
la frontera del sistema: **todo lo que entra se valida aqui**, y a partir de
este punto el resto del codigo trabaja con entidades ya validas.

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

import json
from pathlib import Path
from typing import Any, Mapping

from ..dominio.contrato import SCHEMA, TIPO_AISLADA, TIPO_FRASE
from ..dominio.entidades import Frame, Lado, Mano, Muestra, MuestraAislada, MuestraFrase
from ..dominio.errores import ErrorDeContrato


def _exigir(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise ErrorDeContrato(mensaje)


def _mano_desde_dict(d: Any, ctx: str) -> Mano:
    _exigir(isinstance(d, Mapping), f"{ctx}: una mano debe ser un objeto")
    _exigir("lado" in d, f"{ctx}: falta 'lado'")
    _exigir("lm" in d, f"{ctx}: falta 'lm'")
    lm = d["lm"]
    _exigir(isinstance(lm, list), f"{ctx}: 'lm' debe ser una lista")
    try:
        return Mano(
            lado=Lado.desde_texto(str(d["lado"])),
            score=float(d.get("score", 1.0)),
            lm=tuple(tuple(p) for p in lm),
        )
    except ErrorDeContrato as exc:
        # La entidad ya sabe QUE esta mal; aqui se anade DONDE.
        raise ErrorDeContrato(f"{ctx}: {exc}") from exc
    except (TypeError, ValueError) as exc:
        raise ErrorDeContrato(f"{ctx}: landmarks invalidos ({exc})") from exc


def _frame_desde_dict(d: Any, i: int) -> Frame:
    ctx = f"frame {i}"
    _exigir(isinstance(d, Mapping), f"{ctx}: debe ser un objeto")
    manos = d.get("manos", [])
    _exigir(isinstance(manos, list), f"{ctx}: 'manos' debe ser una lista")
    try:
        t = int(d.get("t", i))
    except (TypeError, ValueError) as exc:
        raise ErrorDeContrato(f"{ctx}: 't' invalido") from exc
    return Frame(
        t=t,
        manos=tuple(_mano_desde_dict(m, f"{ctx}, mano {j}") for j, m in enumerate(manos)),
    )


def muestra_desde_dict(d: Any) -> Muestra:
    """Valida un dict del contrato y lo convierte en entidad.

    Lanza `ErrorDeContrato` con un mensaje accionable ante cualquier
    desviacion. Nunca devuelve una entidad a medias.
    """
    _exigir(isinstance(d, Mapping), "la muestra debe ser un objeto JSON")
    schema = d.get("schema")
    _exigir(schema == SCHEMA, f"schema {schema!r} no soportado (esperado {SCHEMA})")

    frames_json = d.get("frames")
    _exigir(isinstance(frames_json, list), "falta la lista 'frames'")
    frames = tuple(_frame_desde_dict(f, i) for i, f in enumerate(frames_json))

    comunes: dict[str, Any] = {
        "frames": frames,
        "sesion": str(d.get("sesion", "")),
        "fps_aprox": float(d["fps_aprox"]) if d.get("fps_aprox") is not None else None,
        "schema": SCHEMA,
    }

    tipo = str(d.get("tipo", TIPO_AISLADA))
    if tipo == TIPO_AISLADA:
        _exigir("etiqueta" in d, "una muestra aislada necesita 'etiqueta'")
        return MuestraAislada(**comunes, etiqueta=str(d["etiqueta"]))
    if tipo == TIPO_FRASE:
        etiquetas = d.get("etiquetas")
        _exigir(isinstance(etiquetas, list), "una frase necesita 'etiquetas' (lista)")
        return MuestraFrase(**comunes, etiquetas=tuple(str(e) for e in etiquetas))
    raise ErrorDeContrato(
        f"tipo de muestra desconocido: {tipo!r} "
        f"(validos: {TIPO_AISLADA}, {TIPO_FRASE})"
    )


def muestra_a_dict(muestra: Muestra) -> dict[str, Any]:
    """Entidad -> dict del contrato. Inverso exacto de `muestra_desde_dict`."""
    d: dict[str, Any] = {
        "schema": muestra.schema,
        "tipo": muestra.tipo,
        "sesion": muestra.sesion,
        "fps_aprox": muestra.fps_aprox,
        "frames": [
            {
                "t": f.t,
                "manos": [
                    {"lado": m.lado.value, "score": m.score, "lm": [list(p) for p in m.lm]}
                    for m in f.manos
                ],
            }
            for f in muestra.frames
        ],
    }
    if isinstance(muestra, MuestraAislada):
        d["etiqueta"] = muestra.etiqueta
    else:
        d["etiquetas"] = list(muestra.glosas)
    return d


def cargar_muestra(ruta: Path) -> Muestra:
    with Path(ruta).open("r", encoding="utf-8") as fh:
        try:
            crudo = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ErrorDeContrato(f"{ruta}: JSON invalido ({exc})") from exc
    try:
        return muestra_desde_dict(crudo)
    except ErrorDeContrato as exc:
        raise ErrorDeContrato(f"{ruta}: {exc}") from exc


def guardar_muestra(ruta: Path, muestra: Muestra) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as fh:
        json.dump(muestra_a_dict(muestra), fh, ensure_ascii=False)
