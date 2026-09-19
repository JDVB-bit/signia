# 📦 `app/` — La aplicación FastAPI

## 📖 Introducción

El código del servicio, en las mismas capas que el paquete del modelo: la de
fuera conoce a la de dentro y nunca al revés.

```
api/  ──►  dominio/        (esquemas de entrada y salida)
  │
  └──────► infra/  ──►  signia_modelo  (contrato, repositorio, casos de uso)
```

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Responsabilidad |
|---|---|
| [`api/`](api/) | 🌐 Una ruta por archivo, la inyección y el manejo de errores |
| [`dominio/`](dominio/) | 🎯 Qué entra y qué sale de la API (Pydantic) |
| [`infra/`](infra/) | 🔌 Cómo se construye el repositorio del dataset |
| `main.py` | 🛰️ `crear_app()`: CORS, manejadores y montaje de rutas |
| `config.py` | ⚙️ Ajustes por variable de entorno, con valores locales por defecto |

---

## 🎯 Qué problema resuelve

Que el servicio se pueda **probar y mover** sin reescribirlo:

1. **Probar** — `crear_app(ajustes)` devuelve una instancia limpia, así que un
   test no depende de las variables de entorno del proceso.
2. **Mover** — nada sabe si corre en un portátil, en una VM o en un contenedor;
   lo único que cambia son las variables de entorno.
3. **No duplicar el contrato** — la validación de las muestras se delega entera
   al paquete del modelo.

---

## 🔗 Qué dependencias tiene

| Dependencia | Dónde |
|---|---|
| `fastapi`, `starlette` | `main.py`, `api/` |
| `pydantic` | `dominio/esquemas/` |
| `signia_modelo` | `api/muestras.py`, `api/salud.py`, `infra/` |

`config.py` no depende de nada: es `os.environ` y una dataclass.

---

## 🧠 Cómo soluciona el problema

### 🏭 Fábrica en vez de objeto global

```python
def crear_app(configuracion: Ajustes | None = None) -> FastAPI: ...
app = crear_app()   # la que sirve uvicorn
```

Los ajustes viajan en `app.state`, no en una caché del proceso: dos instancias
creadas con configuraciones distintas —el servidor y un test— no se pisan.

### 🚨 Los errores se traducen en un solo sitio

Las rutas no llevan `try/except`. Dejan subir `ErrorDeContrato` y
`api/manejador_de_errores.py` lo convierte en un **422** con el mensaje tal
cual, que ya dice qué muestra del lote falla y por qué.

### 🌍 CORS explícito

El front corre en otro puerto (`5173`), así que sin CORS el navegador bloquea
el `POST`. Los orígenes permitidos son configurables y **no** son `*`.

---

## 🔍 Qué tienen los archivos

### `main.py`

| Elemento | Qué es |
|---|---|
| `crear_app(configuracion)` | Monta CORS, manejadores y los tres enrutadores |
| `ENRUTADORES` | El orden en que salen en `/docs` |
| `METODOS_PERMITIDOS`, `CABECERAS_PERMITIDAS` | Lo justo que necesita el front |
| `app` | La instancia que sirve `uvicorn app.main:app` |

### `config.py`

| Elemento | Qué es |
|---|---|
| `Ajustes` | `datos_dir` y `origenes_cors`, inmutable |
| `ajustes()` | Los del entorno, cacheados (el entorno no cambia en caliente) |
| `ENV_DATOS_DIR`, `ENV_ORIGENES` | Los nombres de las variables, en un solo sitio |

`datos_dir` puede quedarse en `None`: entonces manda el valor por defecto del
paquete del modelo, que es quien define dónde vive el dataset.

---

## 💡 Ejemplos de uso

```bash
venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

En un test, una app con otro dataset:

```python
from app.config import Ajustes
from app.main import crear_app

app = crear_app(Ajustes(datos_dir=str(tmp_path), origenes_cors=("http://localhost:5173",)))
```
