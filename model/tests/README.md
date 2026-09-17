# 🧪 `tests/` — Suite de pytest

## 📖 Introducción

**164 tests** que cubren el paquete entero. La carpeta refleja las capas del
código: una subcarpeta por capa, más el test de conformidad y los fixtures que
comparte con el front.

138 de esos tests **no necesitan torch**: se pueden ejecutar en cualquier equipo
en unos segundos.

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Qué es |
|---|---|
| [`dominio/`](dominio/) | 🎯 Validación de entidades (24 tests) |
| [`aplicacion/`](aplicacion/) | ⚙️ Remuestreo y tensor crudo (35 tests) |
| [`infra/`](infra/) | 🔌 JSON, ficheros, rutas, normalización y ONNX (72 tests) |
| [`fixtures/`](fixtures/) | 📎 Casos compartidos con el test de conformidad de JS |
| `test_conformidad.py` | 🤝 Verifica que los fixtures siguen coincidiendo con el código (33 tests) |
| `conftest.py` | 🔧 Fixtures comunes (`muestra_aislada`, `muestra_frase`, `repo_vacio`) y `sys.path` |
| `factorias.py` | 🏭 Fábricas de manos, frames y muestras válidas |
| `__init__.py` | Hace de `tests` un paquete importable (lo usan las fábricas) |

---

## 🎯 Qué problema resuelve

1. **Cambios silenciosos en el contrato.** Tocar `T`, el redondeo o el orden de
   las ranuras invalida modelos ya entrenados; la suite lo convierte en un fallo
   inmediato.
2. **Datos corruptos aceptados.** La frontera JSON tiene 20 tests dedicados a
   rechazar lo que no cumple el contrato, con mensajes que digan dónde.
3. **Bugs de exportación a ONNX.** Ahí es donde aparecen: el grafo exportado
   podría no calcular lo mismo que el módulo con el que se entrenó.
4. **Necesitar una GPU para desarrollar.** Los marcadores permiten trabajar sin
   torch instalado.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `pytest >= 8` | Ejecutar la suite |
| `numpy` | Comparar tensores |
| `torch`, `onnx`, `onnxruntime` | Solo los tests marcados |

Configuración en [`../pyproject.toml`](../pyproject.toml):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
addopts = "-q --strict-markers"
markers = ["torch: necesita torch instalado", "onnx: necesita onnx y onnxruntime"]
```

`--strict-markers` impide inventarse marcadores: un typo en `@pytest.mark.torhc`
falla en vez de pasar desapercibido.

---

## 🧠 Cómo soluciona el problema

### 🏭 Datos sintéticos deterministas

`factorias.py` define una **mano canónica** con la muñeca en el origen, que se
puede trasladar y escalar. Eso permite comprobar propiedades y no solo valores:

> *la forma no cambia al mover la mano, pero la posición sí*

Los valores son cortos a propósito (`0.02`, `0.03`…) para que los fixtures en
JSON sean legibles y exactos en `float32`.

### 🏷️ Marcadores para el hardware

```bash
pytest                      # los 164
pytest -m "not torch"       # los 138 que no necesitan torch
```

Los módulos que lo requieren usan `pytest.importorskip("torch")`, así que en un
equipo sin torch se saltan en vez de romper la recolección.

### 🔧 Fixtures compartidas

| Fixture | Qué da |
|---|---|
| `muestra_aislada` | Una `MuestraAislada` de 30 frames con mano derecha |
| `muestra_frase` | Una `MuestraFrase` de 90 frames y cuatro glosas |
| `repo_vacio` | Un `RepositorioMuestrasEnDisco` sobre `tmp_path` |

`repo_vacio` usa el `tmp_path` de pytest: **ningún test escribe en el dataset
real**.

---

## 🔍 Qué tienen los archivos

### `conftest.py`

Añade la raíz del proyecto a `sys.path` (así la suite corre sin instalar el
paquete) y define las tres fixtures comunes.

### `factorias.py`

| Función | Devuelve |
|---|---|
| `MANO_CANONICA` | 21 puntos deterministas con la muñeca en el origen |
| `mano(lado, *, score, desplazamiento, escala)` | Una `Mano` trasladada y escalada |
| `frame(t, lados, **kwargs)` | Un `Frame` con esas manos |
| `muestra(n_frames, *, etiqueta, sesion, lados)` | Una `MuestraAislada` |
| `frase(n_frames, *, etiquetas, sesion)` | Una `MuestraFrase` |

### `test_conformidad.py`

Importa `scripts/generar_fixtures.py` sin convertirlo en paquete y comprueba,
por cada fixture: versión del preprocesado, validez de la muestra, índices,
tensor (a `1e-5`) y forma. Además verifica que **no falta ningún caso** y que el
generador es reproducible.

---

## 💡 Ejemplos de uso

```bash
venv/Scripts/python -m pytest                        # todo (164 tests)
venv/Scripts/python -m pytest -m "not torch"         # sin torch (138)
venv/Scripts/python -m pytest tests/infra -k onnx    # un subconjunto
venv/Scripts/python -m pytest -q --collect-only      # ver qué hay, sin ejecutar
```

```python
# Usar las fábricas en un test nuevo
from tests import factorias

def test_algo(muestra_aislada):
    otra = factorias.muestra(12, etiqueta="reposo", lados=())
    assert otra.n_frames == 12
```

> 🚨 Si falla `test_conformidad.py`, **no regeneres los fixtures sin pensar**:
> significa que los tensores han cambiado y que hay que reentrenar y tocar el
> remuestreo de JS a la vez.
