# 🧪 `tests/infra/` — Tests de los adaptadores

## 📖 Introducción

La parte más grande de la suite (**72 tests**): la frontera JSON, el dataset en
disco, la normalización de torch y la paridad con ONNX.

Es donde se concentran los errores caros: datos corruptos que entran, rutas que
escapan de su carpeta y grafos exportados que no calculan lo mismo que el módulo
original.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué verifica | Marcador |
|---|---|---|
| `test_json_contrato.py` | Validación del JSON de entrada e ida y vuelta dict ↔ entidad (17) | — |
| `test_ficheros_json.py` | Guardar/cargar en disco y errores que nombran el fichero (3) | — |
| `test_repo_ficheros.py` | Saneado de rutas, guardado, listado, conteo y `DATOS_DIR` (26) | — |
| `test_normalizacion_torch.py` | Invariancias de la forma, ceros exactos sin mano, sin `NaN` (15) | `torch` |
| `test_exportacion_onnx.py` | Paridad torch ↔ onnxruntime a `1e-5` (11) | `torch`, `onnx` |
| `__init__.py` | Hace de la carpeta un paquete de tests | — |

---

## 🎯 Qué problema resuelve

1. **Datos de fuera.** El JSON lo produce un navegador: puede llegar
   incompleto, con campos de otra versión o directamente corrupto.
2. **Rutas construidas con texto del usuario.** La etiqueta acaba siendo un
   nombre de carpeta: `../../etc` no puede prosperar.
3. **Evaluación deshonesta.** Si `n_clases` se escribiera a mano en vez de
   derivarse del dataset, las métricas mentirían.
4. **Bugs de exportación.** Un grafo que no calcula lo mismo que el módulo con el
   que se entrenó hace que el modelo **funcione en los tests y falle en
   producción**.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `pytest`, `numpy` | Toda la carpeta |
| `torch` | Normalización y exportación (`importorskip`) |
| `onnx`, `onnxruntime` | Exportación |
| `tmp_path` de pytest | Ningún test escribe en el dataset real |

---

## 🧠 Cómo soluciona el problema

### 🛡️ Ataques de ruta como caso de test

```python
@pytest.mark.parametrize("ataque", ["../../etc", r"..\..\windows", "a/b", r"c:\datos"])
def test_neutraliza_rutas(self, ataque):
    limpio = sanear(ataque)
    assert "/" not in limpio and "\\" not in limpio and ".." not in limpio
```

### 🔄 Ida y vuelta exacta

```python
copia = muestra_desde_dict(muestra_a_dict(original))
assert copia == original
```

Si la serialización perdiera un campo, la igualdad falla. Se prueba con muestras
aisladas y con frases.

### 🧮 Invariancias, no números mágicos

La normalización se verifica por lo que **debe cumplir**:

| Propiedad | Por qué importa |
|---|---|
| La forma no cambia al mover la mano | La misma seña en cualquier parte del encuadre |
| La posición **sí** cambia | En LSE dónde se hace la seña es significado |
| La forma no cambia al acercarse | Invariancia a escala |
| La escala **sí** cambia (×2 al doble) | Es la señal de profundidad |
| Mano ausente → ceros exactos | Distinguir ausencia de origen |
| Mano degenerada → sin `NaN` | El grafo no puede envenenarse |

### ⚖️ Paridad torch ↔ onnxruntime

Se exporta el módulo, se ejecuta con los dos motores y se comparan salidas con
0, 1 y 2 manos, y con secuencias de 1, 12, 48 y 120 frames. Además se comprueba
que **lote y tiempo son ejes dinámicos**: el entrenamiento evalúa por lotes y el
navegador, de uno en uno.

---

## 🔍 Qué tienen los archivos

### `test_json_contrato.py`

Clases `TestLectura`, `TestValidacion` y `TestEscrituraYRoundTrip`. Rechaza:
no-objeto, `schema` desconocido, sin `frames`, aislada sin `etiqueta`, frase sin
`etiquetas`, tipo desconocido, lado inválido y `lm` que no es lista. Y comprueba
que el error **sitúa el frame y la mano**.

### `test_ficheros_json.py`

Guardar y cargar desde disco, y que un JSON corrupto o un contrato incumplido
mencionen la ruta del fichero.

### `test_repo_ficheros.py`

Saneado, cumplimiento de los tres puertos, estructura en disco
(`crudo/aisladas/<etiqueta>/`), identificadores únicos por sesión, conteo por
etiqueta, orden de lectura estable, repositorio vacío y precedencia del argumento
sobre `DATOS_DIR`.

### `test_normalizacion_torch.py` y `test_exportacion_onnx.py`

Bloques de 64 valores por mano (`presencia`, `posición`, `escala`, `forma`),
lotes, invariancias, robustez y paridad. `Normalizacion` no debe tener
parámetros entrenables: también se comprueba.

---

## 💡 Ejemplos de uso

```bash
venv/Scripts/python -m pytest tests/infra -v
venv/Scripts/python -m pytest tests/infra -m "not torch"   # sin torch instalado
venv/Scripts/python -m pytest tests/infra -k onnx          # solo la paridad
```

```python
# Las pruebas de disco siempre sobre tmp_path
def test_guardar_y_recuperar_una_aislada(repo_vacio):
    muestra = factorias.muestra()
    repo_vacio.guardar(muestra)
    assert list(repo_vacio.listar(tipo=TIPO_AISLADA)) == [muestra]
```

> ⚠️ `test_exportacion_onnx.py` es el test más lento de la suite (exporta un
> grafo de verdad). Es el precio de detectar los bugs de exportación **antes** de
> que lleguen al navegador.
