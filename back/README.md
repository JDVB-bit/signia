# 🛰️ `back/` — API de SignIA (pendiente, Fase 5)

> Todavía **no hay código**: solo `requirements.txt` con las dependencias fijadas.

## 🎯 Qué hará

El backend **no está en el camino crítico** de la traducción (la etapa 1 corre en el navegador). Sus tareas:

| Método | Ruta | Para qué |
|---|---|---|
| `POST` | `/muestras` | Recibir lotes de muestras crudas desde Entrenamiento |
| `GET` | `/modelos/activo` | Manifest, etiquetas, umbrales y URL del `.onnx` |
| `POST` | `/redactar` | Glosas → español natural con un LLM (la clave vive solo aquí) |
| `POST` | `/entrenamientos` | Reentrenar desde cero como job asíncrono (Fase 7) |
| `GET` | `/salud` | Versión del modelo y del preprocesado |

## 🏛️ Estructura prevista

```
back/app/
  main.py
  api/          endpoints (una ruta por archivo)
  dominio/      esquemas Pydantic e interfaz del repositorio
  infra/        SQLite + ficheros, registro de modelos, cliente LLM
  config.py     todo por variables de entorno
```

## 📄 Archivos actuales

| Archivo | Qué es |
|---|---|
| `requirements.txt` | FastAPI, Pydantic, SQLAlchemy y sus dependencias, con versión fijada |

Plan completo: [`.claude/plan-implementacion.md`](../.claude/plan-implementacion.md), Fases 5, 6b y 7.
