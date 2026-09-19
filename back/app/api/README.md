# 🌐 `api/` — Las rutas

## 📖 Introducción

La capa de entrega: traduce HTTP a llamadas del paquete del modelo y de vuelta.
**Un archivo por ruta**, y ninguna lógica de negocio dentro.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Ruta | Qué hace |
|---|---|---|
| `muestras.py` | `POST /muestras` | Valida el lote entero y lo guarda en el dataset |
| `senas.py` | `GET /senas` | Vocabulario y recuento, contados del dataset |
| `salud.py` | `GET /salud` | Estado, versión del contrato y si se puede escribir |
| `dependencias.py` | — | Los ajustes y el repositorio, inyectados |
| `manejador_de_errores.py` | — | `ErrorDeContrato` → `422` con su mensaje |

---

## 🎯 Qué problema resuelve

Que la API sea **una fachada delgada** y no un segundo sistema. Cada ruta cabe
en la pantalla porque no valida el contrato, no escribe ficheros y no decide
nada: eso ya está escrito y probado en `signia_modelo`.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `fastapi` | `APIRouter`, `Depends`, `status` |
| `..dominio.esquemas` | Qué entra y qué sale |
| `signia_modelo.infra.json_lote` | Validar el lote |
| `signia_modelo.aplicacion.importacion_de_lote` | Guardarlo |

---

## 🧠 Cómo soluciona el problema

### 🔗 Inyección, no construcción

```python
def recibir_lote(lote: LoteEntrante, repositorio: RepositorioInyectado): ...
```

La ruta depende del **puerto** `RepositorioMuestras`, no del adaptador de
disco. Dos consecuencias: cambiar dónde vive el dataset no las toca, y la suite
puede sustituirlo por uno temporal.

### 🧯 Todo o nada

`muestras_desde_lote()` levanta `ErrorDeContrato` **antes** de tocar el disco,
así que un lote con una muestra mala no deja media tanda guardada.

### 📣 El error ya viene escrito

El mensaje sale del paquete del modelo con la posición dentro del lote incluida
y se enseña tal cual. Reescribirlo solo perdería información.

### 🩺 La versión del contrato se publica

`GET /salud` devuelve `schema_de_datos` y `version_preprocesado`. Un backend
vivo que habla otro `schema` es peor que uno caído: acepta las muestras y las
guarda mal.

---

## 💡 Ejemplos de uso

Añadir una ruta nueva son tres pasos:

```python
# api/modelos.py
enrutador = APIRouter(tags=["modelos"])

@enrutador.get("/modelos/activo", response_model=ManifiestoDelModelo)
def modelo_activo(repositorio: RepositorioInyectado): ...
```

```python
# main.py
ENRUTADORES = (salud.enrutador, muestras.enrutador, senas.enrutador, modelos.enrutador)
```

Y su archivo de tests en [`../../tests/`](../../tests/).
