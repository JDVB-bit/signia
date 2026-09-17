# 🛰️ `back/` — API de SignIA (pendiente, Fase 5)

## 📖 Introducción

El servicio que **recibirá las muestras** grabadas en el front, **publicará el
artefacto del modelo**, lanzará los **reentrenamientos** y pondrá la **redacción
con LLM** (etapa 2) detrás de una clave privada.

> ⚠️ **Estado: 🔴 sin código.** Hoy esta carpeta solo fija las dependencias
> elegidas. Mientras tanto, el botón **Enviar** de Entrenamiento descarga un
> JSON: el formato ya es el definitivo, solo cambiará el transporte.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué es |
|---|---|
| `requirements.txt` | 📦 FastAPI, Starlette, Pydantic v2, SQLAlchemy 2 y sus transitivas, con versión fijada |
| `venv/` | 🐍 Entorno virtual local (no versionado) |

---

## 🎯 Qué problema resuelve

El backend **no está en el camino crítico** de la traducción: la etapa 1 corre en
el navegador. Existe para lo que el navegador **no puede** hacer:

1. 📥 **Persistir un dataset compartido** entre sesiones y equipos.
2. 📤 **Publicar el artefacto** (`.onnx` + etiquetas + versión de preprocesado +
   métricas) que el front descarga para inferir.
3. 🏋️ **Orquestar el entrenamiento** como job por lotes, con guardarraíl: un
   modelo nuevo no reemplaza al activo si sus métricas son peores.
4. ✍️ **Redactar** el español natural a partir de las glosas, porque la clave del
   LLM no puede vivir en el cliente.

---

## 🔗 Qué dependencias tiene

```text
fastapi==0.141.1      # framework de la API
starlette==1.4.1      # base ASGI
pydantic==2.13.4      # validación de entrada/salida
SQLAlchemy==2.0.51    # persistencia (SQLite en el arranque)
anyio / greenlet / typing_extensions …   # transitivas
```

Y el paquete [`../model/`](../model/), que se reutiliza tal cual: la validación
del contrato (`infra/json_contrato.py`) y el repositorio del dataset
(`infra/repo_ficheros.py`) ya están escritos y testeados. El backend solo los
expone por HTTP.

> 📌 El backend de producción **no necesita torch**: `pyproject.toml` del modelo
> deja el entrenamiento como extra opcional.

---

## 🧠 Cómo lo resolverá

### 🏛️ Estructura prevista

```
back/app/
  main.py
  api/          endpoints (una ruta por archivo)
  dominio/      esquemas Pydantic e interfaz del repositorio
  infra/        SQLite + ficheros, registro de modelos, cliente LLM
  config.py     todo por variables de entorno
```

Mismas reglas que el modelo: Clean Architecture, persistencia detrás de una
interfaz y un archivo por responsabilidad.

### 🌐 Endpoints previstos

| Método | Ruta | Para qué |
|---|---|---|
| `POST` | `/muestras` | Recibir lotes de muestras crudas desde Entrenamiento |
| `GET` | `/modelos/activo` | Manifiesto, etiquetas, umbrales y URL del `.onnx` |
| `POST` | `/redactar` | Glosas → español natural con un LLM |
| `POST` | `/entrenamientos` | Reentrenar desde cero como job asíncrono (Fase 7) |
| `GET` | `/entrenamientos/{id}` | Estado del job |
| `GET` | `/salud` | Versión del modelo y del preprocesado |

### 🔐 Decisiones ya tomadas

- **Escritura atómica del artefacto** (temporal + `rename`), para que nadie lea
  una carpeta a medio escribir.
- **Rollback**: se conserva el artefacto anterior.
- **`/muestras` y `/entrenamientos` protegidos**: abiertos a internet permitirían
  envenenar el dataset.

---

## 🔍 Qué tiene el archivo actual

`requirements.txt` fija las versiones exactas de todo el árbol de dependencias:
así el entorno del servidor es reproducible y no cambia por debajo entre
despliegues.

---

## 💡 Ejemplos de uso

Preparar el entorno (lo único posible hoy):

```bash
cd back
python -m venv venv
venv/Scripts/pip install -r requirements.txt
```

Cuerpo que aceptará `POST /muestras` — es **exactamente** el JSON que descarga
hoy el botón *Enviar*:

```json
{
  "schema": 1,
  "muestras": [
    {
      "schema": 1,
      "tipo": "aislada",
      "etiqueta": "hola",
      "sesion": "2026-09-20-local",
      "fps_aprox": 29.8,
      "frames": [
        { "t": 0, "manos": [{ "lado": "derecha", "score": 0.98, "lm": [[0.1, 0.2, 0.0]] }] }
      ]
    }
  ]
}
```

Validarlo hoy, sin backend:

```python
from signia_modelo.infra.json_contrato import muestra_desde_dict

muestras = [muestra_desde_dict(m) for m in paquete["muestras"]]
```

Plan completo: [`../.claude/plan-implementacion.md`](../.claude/plan-implementacion.md), Fases 5, 6b y 7.
