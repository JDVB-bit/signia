# `model/` — etapa 1 de SignIA

Convierte **senas** (landmarks de MediaPipe) en **glosas**. No redacta espanol:
eso es la etapa 2 (LLM en el backend, Fase 6b del plan).

El plan completo esta en `.claude/plan-implementacion.md`. El contrato de datos,
que es lo que fija todo lo demas, en [`contrato.md`](contrato.md).

## Estructura

```
signia_modelo/
  dominio/       entidades, constantes del contrato y puertos   (python puro)
  aplicacion/    remuestreo y construccion del tensor crudo     (numpy)
  infra/         JSON, disco, torch/ONNX                        (frameworks)
```

La regla es una sola: **las capas de dentro no importan nada de las de fuera**.
El dominio no sabe que existen los ficheros, ni torch, ni la API. Cambiar disco
por almacenamiento en nube, o torch por otra cosa, es escribir otro adaptador en
`infra/` sin tocar el resto.

## Uso

```bash
# tests (todo el paquete)
venv/Scripts/python -m pytest

# solo lo que no necesita torch
venv/Scripts/python -m pytest -m "not torch"

# regenerar los fixtures de conformidad JS <-> Python
venv/Scripts/python scripts/generar_fixtures.py
```

## Estado

- [x] **Fase 0** — contrato, remuestreo, tensor crudo, normalizacion en el grafo
      ONNX, repositorio del dataset y suite de tests.
- [x] **Fase 1** — captura en el front (`front/app/src/lib/`).
- [ ] Fase 2 — dataset (aisladas + `reposo` + frases de evaluacion).
- [ ] Fase 3 — baseline DTW.
- [ ] Fase 4 — modelo, WER por frase y artefacto.
