# ⚙️ `aplicacion/` — Preprocesado e inspección del dataset

## 📖 Introducción

La capa que convierte una **muestra cruda** en el **tensor de longitud fija** que
entra al grafo ONNX, y la que mide el dataset para saber si ya se puede
entrenar. Depende solo del dominio y de numpy.

**Aquí no se normaliza nada**: restar la muñeca, calcular la escala y dividir
ocurre *dentro* del grafo, que es lo único que garantiza que el navegador y el
entrenamiento hagan exactamente lo mismo.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `remuestreo.py` | ⏱️ De `n` frames a `destino` índices, con `int(x + 0.5)`. Gemelo de `front/app/src/aplicacion/remuestreo.js` |
| `preprocess.py` | 🧱 Muestra → `EntradaCruda(lm (T,2,21,3), presencia (T,2))`, con ranuras fijas |
| [`inspeccion/`](inspeccion/) | 🔬 Métricas, resumen, diagnóstico y trayectoria del dataset (Fase 2) |
| `__init__.py` | Documenta la capa |

El preprocesado alimenta al **modelo**; la inspección alimenta a la **persona
que graba**. Son dos usos del mismo dato y no comparten código.

---

## 🎯 Qué problema resuelve

1. **Duración variable.** Una seña puede durar 0,8 s o 3 s; el modelo espera
   siempre `T = 48` pasos.
2. **Ranuras inestables.** MediaPipe devuelve las manos en el orden que quiere:
   si el tensor siguiera ese orden, la misma seña produciría vectores distintos.
3. **Ausencia de mano.** Hay que distinguir *"no hay mano"* de *"hay una mano en
   el origen"*, o el modelo aprendería que el origen significa reposo.
4. **Divergencia con el navegador.** Es la única lógica duplicada del
   preprocesado, así que se escribe de forma deliberadamente trivial y se vigila
   con fixtures.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `numpy` | Los arrays `float32` del tensor (la inspección **no** lo usa) |
| `..dominio.contrato` | `T`, `N_MANOS`, `N_LANDMARKS`, `N_DIMS`, `LADOS_CANONICOS` |
| `..dominio.entidades` | `Frame`, `Lado`, `Muestra` |
| `..dominio.puertos` | El protocolo `Remuestreador` |

No importa nada de `infra/`: no sabe que existen ficheros, ni torch, ni ONNX.

---

## 🧠 Cómo soluciona el problema

### ⏱️ Elegir frames, nunca interpolar

```
indice(i) = int( i * (n - 1) / (destino - 1) + 0.5 )
```

- Si sobran frames se saltan; si faltan se repiten. Los extremos siempre se
  conservan.
- Interpolar entre un frame con mano y otro sin ella **inventaría medias manos**
  que MediaPipe nunca produjo.
- El redondeo se escribe `int(x + 0.5)` **a propósito**: `round()` de Python
  redondea al par (`round(0.5) == 0`) y `Math.round` de JS no (`1`). Con
  `round()`, navegador y entrenamiento verían tensores distintos y el fallo sería
  silencioso.

### 🖐️ Ranuras canónicas y presencia explícita

| Salida | Forma | Contenido |
|---|---|---|
| `lm` | `(T, 2, 21, 3)` `float32` | Landmarks crudos; ranura `0 = izquierda`, `1 = derecha` |
| `presencia` | `(T, 2)` `float32` | `1.0` si esa mano está, `0.0` si no |

La mano ausente queda en ceros **y** con presencia `0`. Esa segunda señal es la
que distingue ausencia de origen.

### 🔧 Remuestreador inyectable

`construir_entrada` recibe el remuestreador como parámetro con valor por defecto:
el preprocesado depende del **puerto**, no de la estrategia (DIP + OCP).

---

## 🔍 Qué tienen los archivos

### `remuestreo.py`

| Elemento | Detalle |
|---|---|
| `indices_remuestreo(n_frames, destino=T)` | Lista de índices; lanza `ErrorDeRemuestreo` con secuencia vacía o destino inválido |
| `RemuestreadorPorIndices` | Implementación por defecto del puerto; existe como clase para poder sustituirla |
| `REMUESTREADOR_POR_DEFECTO` | Instancia reutilizable (no tiene estado) |

### `preprocess.py`

| Elemento | Detalle |
|---|---|
| `RANURAS` | `(Lado.IZQUIERDA, Lado.DERECHA)`, derivado de `LADOS_CANONICOS` |
| `EntradaCruda` | `NamedTuple` con `lm` y `presencia` |
| `apilar_frames(frames)` | Apila frames **ya elegidos**; no remuestrea |
| `construir_entrada(muestra, *, remuestreador, destino=T)` | Remuestrea y apila |

Separar `apilar_frames` de `construir_entrada` permite probar el apilado sin
remuestreo y, en la Fase 6, alimentar ventanas continuas sin pasar por una
muestra completa.

---

## 💡 Ejemplos de uso

```python
from signia_modelo.aplicacion.preprocess import construir_entrada
from signia_modelo.aplicacion.remuestreo import indices_remuestreo

indices_remuestreo(3, 5)                 # [0, 1, 1, 2, 2]  ← redondeo estilo JS
indices_remuestreo(120)[:5]              # [0, 3, 5, 8, 10]

entrada = construir_entrada(muestra)
entrada.lm.shape                         # (48, 2, 21, 3)
entrada.presencia.shape                  # (48, 2)
entrada.presencia[0]                     # array([0., 1.], dtype=float32)
```

```python
# Ventana más corta (modo continuo, Fase 6)
entrada = construir_entrada(muestra, destino=16)
entrada.lm.shape                         # (16, 2, 21, 3)
```

```python
# Estrategia alternativa, sin tocar el preprocesado
class SiempreElUltimo:
    def indices(self, n_frames, destino):
        return [n_frames - 1] * destino

construir_entrada(muestra, remuestreador=SiempreElUltimo(), destino=4)
```

> 🔒 Si tocas `remuestreo.py`, ejecuta **las dos** suites: `pytest` y, en el
> front, `pnpm test`. Los fixtures de `tests/fixtures/` son la referencia
> compartida.
