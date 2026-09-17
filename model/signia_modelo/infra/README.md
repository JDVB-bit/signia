# 🔌 `infra/` — Adaptadores

## 📖 Introducción

Todo lo que es **"detalle"**: formatos, rutas, variables de entorno y
frameworks. Aquí viven el JSON, el sistema de ficheros, torch y ONNX.

El dominio no importa nada de este paquete; este paquete importa del dominio.
Cambiar disco por nube, o torch por otra cosa, es escribir otro archivo aquí.

---

## 📂 Qué archivos tiene y qué hace cada uno

### 📥 Datos

| Archivo | Responsabilidad |
|---|---|
| `json_contrato.py` | 🔄 dict JSON ↔ entidades, con validación y mensajes accionables |
| `ficheros_json.py` | 💾 Cargar / guardar una muestra en un `.json` |
| `nombres_de_ruta.py` | 🛡️ Sanear etiquetas y sesiones antes de usarlas como carpeta |
| `configuracion_datos.py` | ⚙️ Raíz del dataset por `DATOS_DIR` (por defecto `./data`) |
| `repo_ficheros.py` | 🗂️ El dataset en disco: `crudo/aisladas/<etiqueta>/` y `crudo/frases/` |

### 🧮 Modelo

| Archivo | Responsabilidad |
|---|---|
| `normalizacion_torch.py` | 🧮 Crudo → 128 features como `nn.Module` (viaja **dentro** del ONNX) |
| `exportacion_onnx.py` | 📦 Exporta a ONNX con lote y tiempo como ejes dinámicos |
| `ejecucion_onnx.py` | ▶️ Ejecuta el grafo con onnxruntime, igual que hará el navegador |

---

## 🎯 Qué problema resuelve

1. **La frontera del sistema.** Lo que llega en JSON viene de fuera: se valida
   **una vez**, aquí, y a partir de ahí el resto trabaja con entidades válidas.
2. **Rutas construidas con datos del usuario.** La etiqueta la escribe una
   persona y acaba siendo un nombre de carpeta: `../../etc` no puede pasar.
3. **Despliegues distintos.** Dónde vive el dataset se decide por entorno, no en
   el código.
4. **La deriva entre entrenamiento e inferencia.** Si la normalización se
   escribiera aparte en JS, divergiría en silencio. Metida en el grafo, es
   imposible.

---

## 🔗 Qué dependencias tiene

| Dependencia | Dónde | ¿Obligatoria? |
|---|---|---|
| `json`, `pathlib`, `os`, `re` | Datos | Estándar |
| `numpy` | ONNX | Sí |
| `torch` | `normalizacion_torch.py`, `exportacion_onnx.py` | Solo para entrenar/exportar |
| `onnxruntime` | `ejecucion_onnx.py` (import diferido) | Solo para ejecutar el grafo |

Por eso `pyproject.toml` separa el extra `entrenamiento`: **el backend de
producción no necesita torch**.

---

## 🧠 Cómo soluciona el problema

### 🧅 Un archivo, una responsabilidad

Convertir no es leer, y leer no es decidir dónde:

```
json_contrato.py   dict ↔ entidad        (formato)
ficheros_json.py   fichero ↔ entidad     (E/S)
nombres_de_ruta.py texto → segmento      (seguridad)
configuracion_datos.py  raíz del dataset (despliegue)
repo_ficheros.py   el dataset completo   (organización)
```

Así el repositorio se lee de un vistazo y cada pieza se puede probar sola.

### 🧮 La normalización viaja dentro del grafo

```
JS y Python (idéntico y trivial):  elegir 48 índices → (48,2,21,3) + presencia
Dentro del grafo ONNX:             restar muñeca, escala, dividir → (48,128)
```

`Normalizacion` es un `nn.Module` **sin parámetros entrenables**: solo álgebra.
Se exporta junto al modelo, así que entrenamiento e inferencia ejecutan
literalmente el mismo código.

### 🛡️ Saneado estricto

`sanear()` sustituye todo lo que no sea letra, dígito, guion o guion bajo. Cierra
el paso a `../`, a `\` y a `C:`, y lanza si no queda nada utilizable.

---

## 🔍 Qué tienen los archivos

### `json_contrato.py`

`muestra_desde_dict(d)` valida y construye; `muestra_a_dict(muestra)` es su
inverso exacto (el *round-trip* está testeado). Los errores dicen **dónde**:
`frame 1, mano 0: se esperaban 21 landmarks…`.

### `ficheros_json.py`

`cargar_muestra(ruta)` y `guardar_muestra(ruta, muestra)`, siempre en `utf-8`
(las etiquetas pueden llevar tildes) y creando las carpetas que falten.

### `nombres_de_ruta.py`

`sanear(texto)` → `"Hola Mundo"` se convierte en `hola_mundo`.

### `configuracion_datos.py`

`raiz_de_datos(explicita=None)`: el argumento gana a `DATOS_DIR`, y este al
valor por defecto `./data`.

### `repo_ficheros.py`

| Método | Qué hace |
|---|---|
| `guardar(muestra)` | Escribe y devuelve el identificador (`sesion-0000`) |
| `listar(*, tipo, etiqueta)` | Itera muestras ya validadas |
| `rutas(...)` | Rutas en orden estable (alfabético) |
| `etiquetas()` | Clases presentes en el dataset |
| `contar()` | Muestras por etiqueta |

> 📌 **`n_clases` sale de `etiquetas()`**, nunca se escribe en el código: añadir
> una seña al vocabulario es grabar muestras, no editar una constante.

### `normalizacion_torch.py`

| Función | Salida | Por qué |
|---|---|---|
| `posicion_muneca(lm)` | `(B,T,2,2)` | En LSE **dónde** se hace la seña es significado |
| `escala_mano(lm)` | `(B,T,2)` | Distancia muñeca→nudillo medio: proxy de profundidad |
| `forma_relativa(lm, escala)` | `(B,T,2,60)` | Invariante a traslación y escala |
| `Normalizacion.forward` | `(B,T,128)` | Concatena los cuatro bloques y multiplica por la presencia |

La escala se *clampa* a `EPS_ESCALA` antes de dividir: una mano degenerada no
puede producir `NaN` dentro del grafo.

### `exportacion_onnx.py` y `ejecucion_onnx.py`

`exportar(...)` fija **lote y tiempo como ejes dinámicos**, compartidos entre
`lm` y `presencia`. `salida_onnx(...)` ejecuta en CPU, para que el resultado no
dependa de la GPU del equipo.

---

## 💡 Ejemplos de uso

```python
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco

repo = RepositorioMuestrasEnDisco()            # DATOS_DIR o ./data
identificador = repo.guardar(muestra)          # '2026-09-20-snt-0000'
repo.contar()                                  # {'hola': 1}
repo.etiquetas()                               # ['hola']
```

```python
from signia_modelo.infra.ficheros_json import cargar_muestra
from signia_modelo.infra.json_contrato import muestra_desde_dict

muestra = cargar_muestra("data/crudo/aisladas/hola/2026-09-20-snt-0000.json")
muestra = muestra_desde_dict(paquete["muestras"][0])   # desde una petición HTTP
```

```python
from signia_modelo.infra.ejecucion_onnx import salida_onnx
from signia_modelo.infra.exportacion_onnx import exportar
from signia_modelo.infra.normalizacion_torch import NOMBRES_ENTRADA, NOMBRE_SALIDA, Normalizacion

ruta = exportar(Normalizacion(), (lm, presencia), "artefactos/norm.onnx",
                nombres_entrada=NOMBRES_ENTRADA, nombre_salida=NOMBRE_SALIDA)
features = salida_onnx(ruta, {"lm": lm_np, "presencia": presencia_np})   # (B, T, 128)
```
