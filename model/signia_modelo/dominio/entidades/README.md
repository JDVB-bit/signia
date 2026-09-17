# 🧩 `entidades/` — Lo que es una muestra

## 📖 Introducción

Las seis entidades del dominio, **una por archivo**. Son inmutables
(`frozen=True`) y se validan a sí mismas al construirse: **si existe la
instancia, cumple el contrato**.

Los landmarks se guardan **crudos**, tal como los devuelve MediaPipe. Ninguna
normalización vive aquí (principio 1 del plan).

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Entidad | Regla clave |
|---|---|---|
| `lado.py` | `Lado` | `izquierda` / `derecha` según el *handedness* (la mano **real**, no la del espejo) |
| `mano.py` | `Mano`, `Punto` | 21 landmarks de 3 coordenadas, `score` dentro de `[0, 1]` |
| `frame.py` | `Frame` | 0, 1 o 2 manos; `mano(lado)` elige la de mayor score si hay duplicadas |
| `muestra.py` | `Muestra` | Base: al menos un frame y una `sesion` identificada |
| `muestra_aislada.py` | `MuestraAislada` | Una seña. **Única unidad de entrenamiento** |
| `muestra_frase.py` | `MuestraFrase` | Varias señas. **Nunca entrena**: mide WER y calibra umbrales |
| `__init__.py` | — | Reexporta todas, para importar desde un único sitio |

---

## 🎯 Qué problema resuelve

1. **Datos a medias circulando por el sistema.** Sin validación en el
   constructor, una mano de 5 landmarks viajaría hasta el tensor y reventaría
   lejos de donde se originó.
2. **Comprobaciones repetidas.** Si la entidad se valida sola, la capa de
   aplicación y la de infraestructura no tienen que volver a preguntarse si el
   `score` está en rango.
3. **Mutaciones accidentales.** Un preprocesado que modificara una muestra
   *in situ* contaminaría el resto del entrenamiento sin dejar rastro.
4. **Tratar igual aisladas y frases.** El preprocesado no debería preguntar de
   qué tipo es una muestra para saber cómo leerla.

---

## 🔗 Qué dependencias tiene

Solo biblioteca estándar (`dataclasses`, `enum`) y dos módulos hermanos:
`../contrato.py` y `../errores.py`.

---

## 🧠 Cómo soluciona el problema

### 🛡️ Validación en `__post_init__`

Como los `dataclass` son `frozen`, los valores normalizados se asignan con
`object.__setattr__`. Eso permite aceptar entradas cómodas (el lado como texto,
listas en vez de tuplas) y guardar siempre la forma canónica.

### 🧬 Herencia con sustituibilidad (LSP)

```
Muestra                 ← lo que necesita el preprocesado
├── MuestraAislada      etiqueta:  str          → glosas == (etiqueta,)
└── MuestraFrase        etiquetas: tuple[str]   → glosas == etiquetas
```

La propiedad `glosas` existe en las dos y devuelve **siempre** una secuencia:
por eso el código de arriba nunca pregunta `if isinstance(...)`.

### ⚖️ Una sola regla de desempate

`Frame.mano(lado)` usa `max(..., key=score)`, que conserva la primera ante
empate. Es exactamente la misma regla que `manoDelFrame` en JavaScript, y está
escrita en esos dos sitios y en ninguno más.

---

## 🔍 Qué tienen los archivos

### `lado.py`

`Lado(str, Enum)` con `IZQUIERDA` y `DERECHA`, y el constructor
`Lado.desde_texto(valor)`, que lanza un `ErrorDeContrato` **enumerando los
valores válidos** en el mensaje.

### `mano.py`

| Validación | Error si… |
|---|---|
| Lado | No es un `Lado` válido |
| `score` | Fuera de `[SCORE_MINIMO, SCORE_MAXIMO]` |
| Número de landmarks | Distinto de `N_LANDMARKS` |
| Coordenadas por punto | Distinto de `N_DIMS` (el error dice **qué landmark**) |

### `frame.py`

`t` no puede ser negativo. `manos` se normaliza a tupla. `mano(lado)` devuelve
`Mano | None`.

### `muestra.py`

| Validación | Motivo |
|---|---|
| `schema` esperado | Un formato distinto no se interpreta a ciegas |
| Al menos un frame | Una muestra vacía no es una muestra |
| `sesion` no vacía | **Sin sesión no hay split honesto** en la evaluación (Fase 4) |
| `fps_aprox > 0` si se indica | Un fps de 0 o negativo es un dato corrupto |

Propiedades: `tipo`, `n_frames`, `glosas`.

### `muestra_aislada.py` y `muestra_frase.py`

La aislada exige `etiqueta` no vacía; la frase exige `etiquetas` no vacía y sin
elementos vacíos.

---

## 💡 Ejemplos de uso

```python
from signia_modelo.dominio.entidades import Frame, Lado, Mano, MuestraAislada

mano = Mano(lado=Lado.DERECHA, score=0.97, lm=[(0.1, 0.2, 0.0)] * 21)
muestra = MuestraAislada(
    frames=[Frame(t=0, manos=[mano])],
    sesion="2026-09-20-snt",
    etiqueta="hola",
)
muestra.glosas        # ('hola',)
muestra.n_frames      # 1
muestra.tipo          # 'aislada'
```

```python
from signia_modelo.dominio.entidades import MuestraFrase

frase = MuestraFrase(frames=frames, sesion="2026-09-20-snt", etiquetas=("hola", "como", "estar", "tu"))
frase.glosas          # ('hola', 'como', 'estar', 'tu')   ← misma API que la aislada
```

```python
# Dos manos con el mismo lado: gana la de mayor score
Frame(t=0, manos=[floja, buena]).mano(Lado.DERECHA) is buena   # True
```
