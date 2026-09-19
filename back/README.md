# 🛰️ `back/` — API de SignIA

## 📖 Introducción

El servicio que **recibe las muestras** grabadas en Entrenamiento y publica el
vocabulario del dataset. Más adelante publicará el artefacto del modelo,
lanzará los reentrenamientos y pondrá la redacción con LLM (etapa 2) detrás de
una clave privada.

> 🟢 **Estado: la primera mitad de la Fase 5 funciona.** `POST /muestras`,
> `GET /senas` y `GET /salud` están implementados y testeados. Faltan
> `POST /entrenamientos`, `GET /modelos/activo` y `POST /redactar`: un endpoint
> que lanza un entrenamiento que todavía no existe (`train.py`, Fase 4) no se
> podría ni probar.

El backend **no está en el camino crítico de la traducción**: la etapa 1 correrá
en el navegador. Existe para lo que el navegador no puede hacer — persistir un
dataset compartido, publicar el artefacto, orquestar el entrenamiento y guardar
el secreto del LLM.

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Qué es |
|---|---|
| [`app/`](app/) | 📦 La aplicación, en capas: `api/`, `dominio/`, `infra/` y la configuración |
| [`tests/`](tests/) | 🧪 26 tests de la API con `TestClient`, sobre un dataset temporal |
| `pyproject.toml` | ⚙️ Nombre del proyecto y configuración de pytest |
| `requirements.txt` | 📌 Dependencias fijadas (FastAPI, Pydantic v2, uvicorn…) |
| `venv/` | 🐍 Entorno virtual local (no versionado) |

---

## 🎯 Qué problema resuelve

**El bucle de reentrenamiento no se cerraba.** Grabar producía un fichero que
alguien tenía que mover a mano hasta `model/data/`, y ese paso manual es donde
se pierden muestras, se confunden sesiones y se cuelan etiquetas mal escritas.

| Sin backend | Con `POST /muestras` |
|---|---|
| Descargar, buscar el fichero, ejecutar un script | Pulsar *Enviar* |
| El dataset vive en el portátil de quien graba | Vive en un sitio, compartido |
| Un fichero mal copiado ensucia el dataset en silencio | El lote se valida entero antes de escribir |
| Nadie sabe qué hay grabado sin abrir carpetas | `GET /senas` lo dice |

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `fastapi` + `starlette` | El framework y la base ASGI |
| `pydantic` v2 | Validar **el sobre** de entrada y tipar las respuestas |
| `uvicorn` | Servidor ASGI de desarrollo |
| `httpx` + `pytest` | La suite (el `TestClient` de FastAPI habla por httpx) |
| [`../model/`](../model/) | 📦 **El contrato, el repositorio y el caso de uso de importación** |

El paquete del modelo se instala en modo editable:

```bash
venv/Scripts/pip install -e ../model
```

> 📌 El backend **no necesita torch**: el entrenamiento es un extra opcional del
> `pyproject.toml` del modelo.

---

## 🧠 Cómo lo resuelve

### 🏛️ Estructura en capas

```
back/app/
  main.py        la fábrica `crear_app()` y el montaje de rutas
  config.py      todo por variables de entorno, con defaults locales
  api/           una ruta por archivo + inyección + manejo de errores
  dominio/       esquemas Pydantic: qué entra y qué sale de la API
  infra/         cómo se construye el repositorio del dataset
```

Las mismas reglas que el modelo: Clean Architecture, persistencia detrás de una
interfaz y un archivo por responsabilidad.

### 🚫 El contrato de datos NO se reescribe aquí

Es la decisión de diseño más importante del backend. Pydantic valida que llegue
un sobre `{schema, muestras: [...]}` **y nada más**; quién decide si una muestra
cumple el contrato es `signia_modelo.infra.json_lote`, el mismo código que usa
el importador de consola y que se verifica contra las fixtures compartidas con
el front.

Si el contrato se escribiera también en modelos Pydantic habría **dos
definiciones** de qué es una muestra, y podrían separarse en silencio —
exactamente lo que el test de contrato cruzado existe para impedir.

### ♻️ El endpoint y el script hacen lo mismo

```
front ── POST /muestras ─┐
                         ├─► muestras_desde_lote() ─► importar_lote() ─► dataset
fichero ── importar_lote.py ─┘
```

No hay dos caminos con dos comportamientos: hay un caso de uso y dos formas de
invocarlo. Por eso *Enviar* y el script no pueden divergir.

### 🧯 Todo o nada

Un lote con una muestra inválida se rechaza **entero**, con un 422 que dice qué
muestra y por qué. Media tanda guardada sería peor que ninguna: nadie sabría
cuál falta.

### 🔌 Inyección para no mentir en los tests

Las rutas piden el repositorio por `Depends`, así que la suite lo sustituye por
uno sobre `tmp_path`. **Ningún test puede escribir en el dataset real.**

---

## 🔍 Qué tienen los archivos

### Endpoints de hoy

| Método | Ruta | Devuelve |
|---|---|---|
| `POST` | `/muestras` | `201` con `{guardadas, identificadores, por_etiqueta}` |
| `GET` | `/senas` | `{n_clases, senas: [{etiqueta, muestras}]}` |
| `GET` | `/salud` | `{estado, schema_de_datos, version_preprocesado, dataset_escribible}` |

`GET /salud` publica la versión del contrato **a propósito**: un backend vivo
que habla otro `schema` es peor que uno caído, porque acepta las muestras y las
guarda mal.

### Endpoints previstos

| Método | Ruta | Cuándo |
|---|---|---|
| `GET` | `/modelos/activo` | Cuando exista un artefacto (Fase 4) |
| `POST` | `/entrenamientos` | Cuando exista `train.py` (Fases 4 y 7) |
| `GET` | `/entrenamientos/{id}` | Con el job asíncrono |
| `POST` | `/redactar` | Etapa 2, glosas → español (Fase 6b) |

### Variables de entorno

| Variable | Por defecto | Para qué |
|---|---|---|
| `DATOS_DIR` | `./data` (la del paquete del modelo) | Dónde vive el dataset |
| `SIGNIA_ORIGENES_CORS` | `http://localhost:5173` y su `127.0.0.1` | Orígenes permitidos, separados por comas |

---

## 💡 Ejemplos de uso

Preparar el entorno:

```bash
cd back
python -m venv venv
venv/Scripts/pip install -r requirements.txt
venv/Scripts/pip install -e ../model
```

Levantar la API (con el dataset donde tú quieras):

```bash
DATOS_DIR=../model/data venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

Documentación interactiva en `http://localhost:8000/docs`.

Comprobar que habla tu mismo contrato:

```bash
curl http://localhost:8000/salud
```

```json
{"estado":"ok","schema_de_datos":1,"version_preprocesado":"1","dataset_escribible":true}
```

Subir un lote (es **exactamente** el JSON que descargaba el botón *Enviar*):

```bash
curl -X POST http://localhost:8000/muestras -H "Content-Type: application/json" \
     --data-binary @signia-hola-2026-09-20-local.json
```

```json
{"guardadas":4,"identificadores":["2026-09-20-local-0000","..."],
 "por_etiqueta":{"hola":3,"reposo":1}}
```

Ver qué hay grabado:

```bash
curl http://localhost:8000/senas
```

```json
{"n_clases":2,"senas":[{"etiqueta":"hola","muestras":3},{"etiqueta":"reposo","muestras":1}]}
```

Y un lote inválido no entra a medias:

```json
{"detail":"muestra 1 del lote: falta la lista 'frames'"}
```

Ejecutar la suite:

```bash
venv/Scripts/python -m pytest        # 26 tests, sobre un dataset temporal
```

Plan completo: [`../.claude/plan-implementacion.md`](../.claude/plan-implementacion.md), Fases 5, 6b y 7.
