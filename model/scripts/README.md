# 🛠️ `scripts/` — Utilidades de línea de comandos

## 📖 Introducción

Herramientas que se ejecutan a mano, fuera del paquete y fuera de los tests. Hoy
hay una: la que **genera la referencia compartida** entre el preprocesado de
Python y el de JavaScript.

Según avance el plan, aquí vivirán también el inspector del dataset (Fase 2), el
baseline DTW (Fase 3) y los scripts de entrenamiento y exportación (Fase 4).

---

## 📂 Qué archivos tiene y qué hace cada uno

| Script | Qué hace |
|---|---|
| `generar_fixtures.py` | 🔁 Regenera `tests/fixtures/*.json`: las muestras límite y el tensor que produce Python |

---

## 🎯 Qué problema resuelve

El test de conformidad necesita una **referencia** que los dos lenguajes puedan
leer. Escribir esos tensores a mano sería inviable (un fixture tiene 6.048
valores de `lm`) y además absurdo: la referencia debe salir del código que
realmente se usa.

Este script convierte esa referencia en algo **reproducible**: un comando, el
mismo resultado.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `signia_modelo.aplicacion` | `construir_entrada`, `indices_remuestreo` |
| `signia_modelo.dominio` | `T`, `VERSION_PREPROCESADO`, entidades |
| `signia_modelo.infra.json_contrato` | Serializar la muestra al formato del contrato |
| `tests.factorias` | La mano canónica |

Reutilizar las fábricas de los tests es deliberado: **la mano de referencia debe
estar definida en un único sitio**.

---

## 🧠 Cómo soluciona el problema

### 🎯 Casos elegidos, no aleatorios

`casos()` construye seis muestras que cubren lo que puede romper el remuestreo:

| Caso | Qué fuerza |
|---|---|
| `un_frame` | Repetir un único frame 48 veces |
| `corta_12` | Repetir frames sin saltarse ninguno |
| `exacta_48` | La identidad |
| `larga_120` | Saltar frames repartiendo uniformemente |
| `sin_manos` | Presencia 0 en toda la secuencia |
| `intermitente` | Mano que entra tarde, cambia de lado y acaba siendo dos |

El caso `intermitente` es el más realista: durante los 8 primeros frames no hay
mano (todavía entrando en el encuadre), luego derecha, luego izquierda, y al
final las dos.

### 🔒 Salida determinista

Las coordenadas se redondean a 6 decimales antes de escribirse: así el JSON es
estable byte a byte y `test_el_generador_es_reproducible` puede compararlo
directamente con lo que hay en disco.

### 📐 Sin `sys.path` mágico en el paquete

El script inserta la raíz del proyecto en `sys.path` **él mismo**, para poder
ejecutarse sin instalar el paquete y sin que el paquete tenga que saber nada de
scripts.

---

## 🔍 Qué tiene el archivo

| Función | Qué hace |
|---|---|
| `casos()` | Devuelve `{nombre: MuestraAislada}` con los seis casos límite |
| `fixture(nombre, muestra)` | Construye el dict del fixture: muestra + índices + presencia + `lm` |
| `main()` | Escribe cada fixture en `tests/fixtures/` e informa por consola |
| `CARPETA`, `DECIMALES` | Destino (`tests/fixtures`) y precisión (6) |

---

## 💡 Ejemplos de uso

```bash
cd model
venv/Scripts/python scripts/generar_fixtures.py
```

Salida:

```
tests\fixtures\un_frame.json  (1 frames)
tests\fixtures\corta_12.json  (12 frames)
tests\fixtures\exacta_48.json  (48 frames)
tests\fixtures\larga_120.json  (120 frames)
tests\fixtures\sin_manos.json  (20 frames)
tests\fixtures\intermitente.json  (35 frames)
```

Y después, **siempre**, las dos suites:

```bash
venv/Scripts/python -m pytest
cd ../front/app && pnpm test
```

> ⚠️ Regenerar los fixtures solo cuando el preprocesado cambie **a propósito**.
> Hacerlo para "arreglar" un test en rojo esconde justo el fallo que el test
> existe para detectar.
