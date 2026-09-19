# 🧪 `tests/aplicacion/inspeccion/` — Tests del inspector del dataset

## 📖 Introducción

Cuatro archivos, uno por módulo de
[`aplicacion/inspeccion/`](../../../signia_modelo/aplicacion/inspeccion/). Son
**66 tests** que corren en milisegundos y sin dataset real: todo el dato se
fabrica con [`tests/factorias.py`](../../factorias.py).

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Módulo que verifica |
|---|---|
| `test_metricas_de_muestra.py` | `metricas_de_muestra.py` — presencia de manos, bimanualidad, duración |
| `test_resumen_del_dataset.py` | `resumen_del_dataset.py` — agrupación, agregados, frases |
| `test_diagnostico_del_dataset.py` | `diagnostico_del_dataset.py` — qué bloquea, qué avisa y qué no |
| `test_trayectoria_de_muneca.py` | `trayectoria_de_muneca.py` — elección de mano, huecos, recorrido |
| `__init__.py` | Hace de la carpeta un paquete (pytest importa por ruta) |

---

## 🎯 Qué problema resuelve

El inspector es **la puerta de la Fase 2**: si dice que el dataset está listo y
no lo está, se entrena con dato malo y el error se atribuye al modelo. Un
inspector equivocado es peor que no tener inspector, porque da confianza falsa.

Estos tests fijan dos cosas:

1. **Que no haya falsos verdes** — el criterio salta cuando debe.
2. **Que no haya falsos rojos** — lo legítimo no se marca como problema
   (`reposo` con las manos bajadas, la misma frase grabada en dos sesiones,
   justo el mínimo de muestras).

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `pytest` | Ejecutar y parametrizar |
| `tests.factorias` | Manos, frames, muestras y frases sintéticas y deterministas |
| `signia_modelo.dominio.criterios_dataset` | Los umbrales, **importados y no copiados** |

No hay mocks ni ficheros temporales: la capa de aplicación no toca disco.

---

## 🧠 Cómo soluciona el problema

### 🟢 Un dataset sano como referencia

`test_diagnostico_del_dataset.py` construye `dataset_sano()`: dos señas más
`reposo`, dos sesiones cada una y frases con secuencias distintas. El primer
test exige que **no tenga ningún aviso**.

Los demás tests parten de ese dataset y **le rompen una cosa**:

```python
muestras = [m for m in dataset_sano() if _no_es_de(m, "reposo")]
assert CodigoDeAviso.SIN_REPOSO in codigos(muestras)
```

Así cada test demuestra que el aviso lo provoca *eso* y no otra cosa.

### 📐 El criterio, no el número

Los umbrales se importan del dominio y se calculan a partir de ellos:

```python
muestras += aisladas("tu", MUESTRAS_MINIMAS_POR_CLASE - 2, sesion="s1")
```

Si mañana el mínimo pasa de 30 a 50, estos tests siguen valiendo. Lo que se
prueba es *"por debajo del mínimo avisa"*, no *"con 28 avisa"*.

### 🚧 Los bordes, explícitos

| Test | Borde que fija |
|---|---|
| `test_justo_el_minimo_de_muestras_no_avisa` | El criterio es "al menos", no "más de" |
| `test_un_dataset_de_solo_reposo_no_exige_factor` | Sin otras clases no hay con qué comparar |
| `test_se_compara_con_la_clase_mas_poblada_no_con_la_media` | Con la media, una clase enorme colaría |
| `test_grabar_cada_frase_dos_veces_es_legitimo` | Repetir en otra sesión es dato bueno |
| `test_en_reposo_las_manos_bajadas_no_son_un_problema` | Ahí la ausencia de mano **es** la clase |
| `test_un_frame_suelto_con_dos_manos_no_la_hace_bimanual` | La otra mano de paso no cuenta |
| `test_ante_un_empate_gana_el_primer_lado_canonico` | Dos ejecuciones dibujan la misma mano |

### 🔁 Orden estable

`test_es_estable_entre_ejecuciones` compara dos diagnósticos del mismo dataset.
Si el orden bailara, el informe sería distinto cada vez y no se podría comparar
entre sesiones de grabación.

---

## 💡 Ejemplos de uso

```bash
cd model
venv/Scripts/python -m pytest tests/aplicacion/inspeccion -q      # los 66
venv/Scripts/python -m pytest tests/aplicacion/inspeccion -k reposo
venv/Scripts/python -m pytest tests/aplicacion/inspeccion -v      # leer los nombres
```

Añadir un criterio nuevo al diagnóstico significa añadir aquí su pareja de
tests: uno que lo dispare y otro que demuestre que no salta cuando no toca.

```python
def test_mi_criterio_salta_cuando_debe(self):
    muestras = [m for m in dataset_sano() if _no_es_de(m, "tu")]
    assert CodigoDeAviso.MI_CODIGO in codigos(muestras)

def test_mi_criterio_no_salta_en_el_dataset_sano(self):
    assert CodigoDeAviso.MI_CODIGO not in codigos(dataset_sano())
```
