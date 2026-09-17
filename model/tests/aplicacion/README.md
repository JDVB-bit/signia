# 🧪 `tests/aplicacion/` — Tests del preprocesado

## 📖 Introducción

Verifican las dos piezas de la capa de aplicación: el **remuestreo temporal** y
la **construcción del tensor crudo**. 35 tests que corren sin torch y en
milisegundos.

El remuestreo se prueba con especial insistencia porque es la única lógica que
existe **dos veces** en el proyecto (Python y JavaScript).

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué verifica |
|---|---|
| `test_remuestreo.py` | Longitud, extremos, monotonía, identidad, reparto uniforme, redondeo `int(x+0.5)`, errores y cumplimiento del puerto (26 tests) |
| `test_preprocess.py` | Ranuras fijas, presencia honesta, mano ausente en ceros, inyección del remuestreador y orden temporal (9 tests) |
| `__init__.py` | Hace de la carpeta un paquete de tests |

---

## 🎯 Qué problema resuelve

1. **La deriva con el navegador.** Si el redondeo cambiara, los dos lados verían
   tensores distintos **sin ningún error visible**.
2. **Perder los extremos de la seña.** Si el remuestreo no conservara el primer
   y el último frame, todas las muestras quedarían recortadas.
3. **Confundir ausencia con origen.** Una mano ausente tiene que salir en ceros
   **y** con presencia `0`.
4. **Que el orden de detección se filtre al tensor.** La ranura la manda el
   `lado`, nunca el orden en que MediaPipe devolvió las manos.

---

## 🔗 Qué dependencias tiene

- `pytest` y `numpy`.
- `signia_modelo.aplicacion` y `signia_modelo.dominio`.
- `tests.factorias` y las fixtures de `conftest.py`.

---

## 🧠 Cómo soluciona el problema

### 🎯 Propiedades, no valores sueltos

```python
@pytest.mark.parametrize("n", [1, 2, 17, 47, 48, 49, 200])
def test_siempre_devuelve_destino_indices(n):
    assert len(indices_remuestreo(n, T)) == T
```

Se prueban invariantes con muchos tamaños —incluidos los tres alrededor de `T`—
en vez de un único caso feliz.

### 🔬 El caso mínimo que distingue los dos redondeos

```python
def test_redondeo_hacia_arriba_como_math_round_de_js():
    # round() de Python (al par) daría [0, 0, 1, 2, 2]
    assert indices_remuestreo(3, 5) == [0, 1, 1, 2, 2]
```

Es el test que impide el bug más caro del proyecto.

### 🧪 Doble del puerto, no de la implementación

```python
class RemuestreadorFalso:
    def indices(self, n_frames, destino):
        return [n_frames - 1] * destino     # siempre el último frame
```

Comprobar que `construir_entrada` lo respeta demuestra que depende del **puerto**
(DIP), y no de la estrategia concreta.

---

## 🔍 Qué tienen los archivos

### `test_remuestreo.py`

| Caso | Lo que garantiza |
|---|---|
| Longitud `T` para cualquier `n` | La ventana es siempre fija |
| Índices en rango y no decrecientes | No se altera el orden temporal |
| Conserva los extremos | La seña no se recorta |
| `n == T` es la identidad | Ningún trabajo innecesario |
| `n == 1` repite ese frame | Caso degenerado resuelto |
| `n == 5` no se salta ninguno | Con pocos frames se repite, no se descarta |
| `n == 95` reparte sin tirones | Saltos de 2-3 frames como mucho |
| Errores | Secuencia vacía y `destino` inválido |
| `isinstance(..., Remuestreador)` | La implementación por defecto cumple el puerto |
| Determinismo | Dos llamadas idénticas dan lo mismo |

### `test_preprocess.py`

| Caso | Lo que garantiza |
|---|---|
| `RANURAS == (IZQUIERDA, DERECHA)` | Orden canónico |
| Formas y `dtype` | `(48,2,21,3)` y `(48,2)` en `float32` |
| Una sola mano | La otra ranura queda en ceros con presencia 0 |
| Frame sin manos | Presencia `[0, 0]` |
| Orden de detección irrelevante | Dos órdenes producen el mismo tensor |
| Landmarks sin tocar | **Aquí no se normaliza nada** (principio 1) |
| `destino` distinto de `T` | Sirve para ventanas continuas |
| Remuestreador inyectado | Se respeta |
| Orden temporal | Las `x` crecen si la mano se desplaza |

---

## 💡 Ejemplos de uso

```bash
venv/Scripts/python -m pytest tests/aplicacion -v
venv/Scripts/python -m pytest tests/aplicacion -k redondeo
```

Ciclo completo al tocar el preprocesado a propósito:

```bash
venv/Scripts/python scripts/generar_fixtures.py
venv/Scripts/python -m pytest
cd ../front/app && pnpm test
```
