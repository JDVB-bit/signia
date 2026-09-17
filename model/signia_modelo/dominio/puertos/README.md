# 🔌 `puertos/` — Interfaces del dominio

## 📖 Introducción

Los contratos que el dominio **necesita que alguien cumpla**, sin saber quién.
Están escritos como `Protocol` de Python: quien los implementa no hereda de nada
y ni siquiera tiene que importarlos.

Es la pieza que permite que el dominio no dependa del disco, de la nube ni de
ninguna estrategia concreta.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Puerto | Implementación actual |
|---|---|---|
| `remuestreador.py` | `Remuestreador.indices(n_frames, destino)` | `aplicacion/remuestreo.py → RemuestreadorPorIndices` |
| `repositorio_muestras.py` | `LectorMuestras`, `EscritorMuestras`, `RepositorioMuestras` | `infra/repo_ficheros.py → RepositorioMuestrasEnDisco` |
| `__init__.py` | Reexporta los cuatro | — |

---

## 🎯 Qué problema resuelve

1. **Que el dominio dependa del disco.** Sin puertos, el preprocesado importaría
   el repositorio de ficheros, y la capa interna acabaría sabiendo que existen
   las carpetas.
2. **Que cambiar de almacenamiento sea una cirugía.** Migrar a GCS o a una base
   de datos debe ser **escribir otro adaptador**, no tocar el dominio.
3. **Que una estrategia quede cementada.** Hoy el remuestreo elige índices
   uniformes; mañana podría centrarse en el pico de movimiento. Debe poder
   sustituirse sin tocar el preprocesado (OCP).
4. **Interfaces gordas.** Quien solo lee muestras no debería arrastrar la firma
   de guardarlas (ISP).

---

## 🔗 Qué dependencias tiene

- `typing` (`Protocol`, `runtime_checkable`, `Iterator`, `Sequence`).
- `..entidades` para tipar `Muestra`.

Nada más: son declaraciones, no implementaciones.

---

## 🧠 Cómo soluciona el problema

### 🔄 Inversión de dependencias (DIP)

```
aplicacion/preprocess.py ──► puertos.Remuestreador   (abstracción)
                                      ▲
                        aplicacion/remuestreo.py     (implementación)
```

La capa de arriba y la de abajo dependen de la **abstracción**. Como son
`Protocol` estructurales, la implementación no necesita declarar que los cumple:
basta con tener el método con la firma correcta.

### 🧩 Segregación (ISP)

```
LectorMuestras     (listar)
EscritorMuestras   (guardar)
       └── RepositorioMuestras = los dos, para quien necesita ambas mitades
```

Un script de inspección pide `LectorMuestras`: así queda escrito en la firma que
**no va a escribir nada**.

### ✅ `runtime_checkable`

Permite a los tests comprobar el cumplimiento de verdad:

```python
assert isinstance(RepositorioMuestrasEnDisco(tmp_path), RepositorioMuestras)
```

---

## 🔍 Qué tienen los archivos

### `remuestreador.py`

```python
class Remuestreador(Protocol):
    def indices(self, n_frames: int, destino: int) -> Sequence[int]: ...
```

Es **la única pieza del preprocesado escrita dos veces** (Python y JS); por eso
está detrás de una interfaz y sometida a un test de conformidad.

### `repositorio_muestras.py`

| Puerto | Método | Devuelve |
|---|---|---|
| `LectorMuestras` | `listar(*, tipo=None, etiqueta=None)` | `Iterator[Muestra]` |
| `EscritorMuestras` | `guardar(muestra)` | `str` — identificador estable |
| `RepositorioMuestras` | ambos | — |

---

## 💡 Ejemplos de uso

```python
from signia_modelo.dominio.puertos import LectorMuestras

def contar_aisladas(repo: LectorMuestras) -> int:
    """Funciona con disco, con GCS o con un repositorio en memoria."""
    return sum(1 for _ in repo.listar(tipo="aislada"))
```

```python
from signia_modelo.aplicacion.preprocess import construir_entrada

class RemuestreadorCentrado:
    """Otra estrategia: centrar la ventana en el pico de movimiento."""
    def indices(self, n_frames: int, destino: int) -> list[int]:
        ...

entrada = construir_entrada(muestra, remuestreador=RemuestreadorCentrado())
```

> 💡 Para añadir un puerto: un archivo por interfaz, con el nombre de lo que
> abstrae, y reexportarlo en `__init__.py`. Si un puerto crece con métodos que
> solo usa un cliente, probablemente sean **dos** puertos.
