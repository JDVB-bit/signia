# 🔬 `inspeccion/` — ¿Sirve el dataset que estamos grabando?

## 📖 Introducción

Cuatro módulos de la **capa de aplicación** que contestan, con números, la
pregunta que abre la Fase 2 del plan: *¿ya hay dato suficiente y bueno para
entrenar?*

Ninguno toca disco, imprime ni depende de torch. Reciben entidades del dominio
y devuelven datos: eso los hace testeables sin dataset real y reutilizables
desde un script, desde el backend o desde un CI.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responde a | Devuelve |
|---|---|---|
| `metricas_de_muestra.py` | ¿Qué hay dentro de **esta** muestra? | `MetricasDeMuestra` |
| `resumen_del_dataset.py` | ¿Cuánto hay de cada clase, y de qué sesiones? | `ResumenDelDataset` |
| `diagnostico_del_dataset.py` | ¿Cumple los criterios de la Fase 2? | `tuple[Aviso, ...]` |
| `trayectoria_de_muneca.py` | ¿La seña **tiene pinta** de seña? | `Trayectoria` |
| `__init__.py` | Reexporta todo lo público, para importar desde un solo sitio | — |

La presentación va aparte: [`infra/informe_de_dataset.py`](../../infra/informe_de_dataset.py)
convierte esto en texto y [`scripts/inspeccionar.py`](../../../scripts/inspeccionar.py)
lo imprime.

---

## 🎯 Qué problema resuelve

El dataset es **el activo irreemplazable** del proyecto y el único paso que no
se puede rehacer sin volver a convocar a la gente. Sin una herramienta que lo
mire, los fallos aparecen tarde y caros:

| Sin inspector | Cuándo se descubre |
|---|---|
| Una clase con la mitad de muestras que las demás | Al entrenar: el modelo la confunde siempre |
| `reposo` con tan pocas muestras como una seña normal | En modo continuo: el segmentador no corta |
| Todo grabado en una sola sesión | En la demo: funciona en casa y no en clase |
| Muestras en las que MediaPipe perdió la mano | Nunca: entran como ceros y bajan la precisión sin explicación |
| Una glosa en las frases que no tiene clase entrenada | Al medir WER: un error que no es del modelo |

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `dominio.entidades` | `Muestra`, `Frame`, `Lado` — lo que se mide |
| `dominio.criterios_dataset` | Los umbrales de la Fase 2, en un solo sitio |
| `dominio.reposo` | La única etiqueta que el código nombra, y por qué |
| `dominio.etiquetas` | La forma canónica: `"Hola"` y `"hola"` son la misma clase |
| `dominio.contrato` | `IDX_MUNECA`, `TIPO_AISLADA`, `TIPO_FRASE` |

**Nada más**: ni numpy, ni torch, ni `pathlib`. Es aritmética sobre entidades.

---

## 🧠 Cómo soluciona el problema

### 📏 Medir y juzgar son dos cosas distintas

`resumen_del_dataset` **no conoce ningún umbral**. Cuenta. Quien juzga es
`diagnostico_del_dataset`, que lee los criterios del dominio. Así subir el
mínimo de 30 a 50 muestras no toca ni una línea del recuento.

### 🔤 Códigos, no frases

El diagnóstico devuelve `CodigoDeAviso.CLASE_CON_POCAS_MUESTRAS`, no *"'hola'
tiene 12 muestras"*. La misma regla vale entonces para la consola, para un
endpoint y para el front, sin reescribirla. Es la misma decisión que en el front
con los motivos de descarte.

### ➕ Un criterio, una función

```python
REVISIONES = (_dataset_vacio, _muestras_por_clase, _reposo, …)
```

Añadir un criterio es añadir una función a esa tupla (OCP). Y el **alcance** se
inyecta: quien mira una sola clase pasa `REVISIONES_DE_CADA_MUESTRA`, porque
sobre media clase no se puede afirmar que falte `reposo`.

### 🧮 Los promedios no bastan, y se sabe

`ResumenDeClase` guarda las medidas **una por una**, no solo la media. Por eso
el aviso puede decir `hola #32` en vez de *"la media se desvió"*: `#32` es el
32.º fichero de esa carpeta en orden alfabético, así que se encuentra a mano.

### 👁️ Y aun así, hay que mirarlo

Una muestra con 40 frames y mano en todos puede ser una seña o una persona
rascándose. `trayectoria_de_muneca` saca el recorrido de la muñeca frame a
frame; el lienzo de infra lo pinta con el tiempo en el carácter, así que se ve
la **dirección** del movimiento, no solo su forma.

---

## 🔍 Qué tienen los archivos

### `metricas_de_muestra.py`

| Miembro | Qué es |
|---|---|
| `medir(muestra)` | Un solo recorrido de los frames → todas las métricas |
| `MetricasDeMuestra.frames_con_alguna_mano` | Frames en los que MediaPipe encontró algo |
| `.frames_por_lado` | Cuántos frames tiene cada mano, en orden canónico |
| `.proporcion_con_mano` | Fracción de la grabación con mano detectada |
| `.usa_las_dos_manos` | ¿Seña bimanual? Se decide por **mayoría de frames**, no por un frame suelto |
| `.segundos` | Duración real, o `None` si la grabación no reportó fps |

Trabaja sobre `Muestra`, la base común: sirve igual para una seña aislada y para
una frase (LSP).

### `resumen_del_dataset.py`

| Miembro | Qué es |
|---|---|
| `resumir(muestras)` | Agrupa por etiqueta normalizada; las frases van aparte |
| `ResumenDeClase` | Las medidas de una seña + agregados (`media_de_frames`, `sesiones`, `muestras_bimanuales`…) |
| `ResumenDeFrases` | `n_frases`, `ordenes_distintos`, `glosas_usadas`, `media_de_glosas` |
| `ResumenDelDataset.n_clases` | **Sale del dataset**, nunca de una constante |
| `.clase(etiqueta)` / `.clases_salvo(etiqueta)` | Para comparar `reposo` con el resto |

Las clases salen **ordenadas alfabéticamente**, igual que en disco: el informe
no puede cambiar entre dos ejecuciones.

### `diagnostico_del_dataset.py`

| Código | Gravedad | Qué detecta |
|---|---|---|
| `DATASET_VACIO` | 🔴 bloquea | No hay nada grabado |
| `CLASE_CON_POCAS_MUESTRAS` | 🔴 bloquea | Menos de `MUESTRAS_MINIMAS_POR_CLASE` |
| `SIN_REPOSO` | 🔴 bloquea | Falta el segmentador |
| `REPOSO_NO_SOBRERREPRESENTADO` | 🔴 bloquea | `reposo` no llega al doble de la clase más poblada |
| `POCAS_SESIONES` | 🔴 bloquea | Todo de una sola sesión |
| `POCAS_FRASES` | 🔴 bloquea | Sin frases no hay WER |
| `GLOSA_DE_FRASE_SIN_CLASE` | 🔴 bloquea | Una frase usa una glosa que nadie entrenó |
| `CLASE_DE_UNA_SOLA_SESION` | 🟠 atención | Esa seña se grabó una sola vez |
| `MUESTRA_DEMASIADO_CORTA` | 🟠 atención | Tan corta que el remuestreo la deja estática |
| `MUESTRA_CON_POCA_MANO` | 🟠 atención | MediaPipe perdió la mano medio clip |
| `FRASES_POCO_VARIADAS` | 🟠 atención | Se repite la misma secuencia |
| `FRASE_DEMASIADO_CORTA` | 🟠 atención | Una sola glosa: no hay transición que medir |
| `CLASE_SIN_FRASES` | 🟠 atención | Se entrena pero nunca se evalúa en continuo |

`reposo` está exenta del criterio de mano: ahí **las manos bajadas son dato
legítimo**, no un fallo de detección.

### `trayectoria_de_muneca.py`

| Miembro | Qué es |
|---|---|
| `trayectoria_de_muneca(muestra, lado=None)` | Recorrido de la muñeca; sin `lado`, el que más aparece |
| `lado_mas_presente(muestra)` | La mano que sale en más frames (determinista ante empate) |
| `Trayectoria.puntos` | Un `(x, y)` por frame, o `None` si esa mano no estaba |
| `.presentes` / `.esta_vacia` | Solo los frames con mano / ¿no hay ninguno? |

Los huecos **no se rellenan**: el hueco en el trazo es la información.

---

## 💡 Ejemplos de uso

```python
from signia_modelo.aplicacion.inspeccion import diagnosticar, resumir
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco

repo = RepositorioMuestrasEnDisco()
resumen = resumir(repo.listar())

print(resumen.n_clases, "clases y", resumen.n_muestras, "muestras")
for aviso in diagnosticar(resumen):
    print(aviso.gravedad.value, aviso.codigo.value, aviso.sujeto)
```

Medir una sola muestra:

```python
from signia_modelo.aplicacion.inspeccion import medir

metricas = medir(muestra)
if metricas.proporcion_con_mano < 0.5:
    print("MediaPipe perdio la mano en media grabacion")
```

Y para verla, desde la línea de comandos:

```bash
venv/Scripts/python scripts/inspeccionar.py --trayectoria hola --muestra 3
```
