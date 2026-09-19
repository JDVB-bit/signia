# 📐 `esquemas/` — Los modelos Pydantic de la API

## 📖 Introducción

Un archivo por recurso, con el mismo criterio que el resto del proyecto: el
nombre del archivo dice de qué habla.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Modelo | Dónde se usa |
|---|---|---|
| `lote.py` | `LoteEntrante` | Cuerpo de `POST /muestras` |
| `importacion.py` | `RespuestaDeImportacion` | Respuesta de `POST /muestras` |
| `sena.py` | `SenaDelVocabulario`, `VocabularioDelDataset` | Respuesta de `GET /senas` |
| `salud.py` | `EstadoDelServicio` | Respuesta de `GET /salud` |
| `__init__.py` | Reexporta los cuatro, para importar desde un solo sitio |

---

## 🎯 Qué problema resuelve

1. **Documentación que no miente** — `/docs` se genera de aquí, así que no se
   queda vieja.
2. **Respuestas estables** — el front sabe qué campos existen y con qué nombre.
3. **No duplicar el contrato de datos** — ver la nota de `lote.py`.

---

## 🔗 Qué dependencias tiene

`pydantic` v2 (`BaseModel`, `Field`).

---

## 🧠 Cómo soluciona el problema

### 📦 `LoteEntrante` valida el sobre y **solo** el sobre

```python
schema_: int = Field(alias="schema")
muestras: list[dict[str, Any]] = Field(min_length=1)
```

`muestras` es una lista de diccionarios **a propósito**: describirlas aquí
crearía una segunda definición del contrato, que podría separarse en silencio de
la de Python y la del front.

El campo se llama `schema_` porque `schema` choca con un atributo de Pydantic;
el alias hace que por HTTP siga siendo `schema`.

### ✅ La respuesta cuenta lo que entró

`RespuestaDeImportacion` no devuelve un `"ok"`: devuelve cuántas muestras
entraron, sus identificadores y el conteo por etiqueta, para que el front pueda
confirmar en pantalla que subió lo que se acababa de grabar.

### 🔢 `n_clases` se cuenta, no se declara

`VocabularioDelDataset.n_clases` sale de contar lo que hay en el dataset. Es el
mismo principio que sostiene el vocabulario abierto del plan: ese número no se
escribe en ninguna parte del código.

---

## 💡 Ejemplos de uso

```python
RespuestaDeImportacion(
    guardadas=4,
    identificadores=["2026-09-20-local-0000", "2026-09-20-local-0001"],
    por_etiqueta={"hola": 3, "reposo": 1},
)
```
