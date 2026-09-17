# 🛠️ `scripts/` — Utilidades de línea de comandos

## 📖 Introducción

Herramientas que se ejecutan a mano, fuera del paquete y fuera de los tests. Hoy
son dos, y las dos **generan la referencia compartida** con el front: una los
tensores, la otra las constantes.

Según avance el plan, aquí vivirán también el inspector del dataset (Fase 2), el
baseline DTW (Fase 3) y los scripts de entrenamiento y exportación (Fase 4).

---

## 📂 Qué archivos tiene y qué hace cada uno

| Script | Qué hace |
|---|---|
| `generar_fixtures.py` | 🔁 Regenera `tests/fixtures/*.json`: las muestras límite y el tensor que produce Python |
| `exportar_contrato.py` | 📜 Regenera `../contrato.json`: las constantes de `dominio/contrato.py` en formato legible por JS |

---

## 🎯 Qué problema resuelve

El front y el entrenamiento tienen que calcular **lo mismo**, y hay dos formas
de que dejen de hacerlo:

| Divergencia | Quién la detecta |
|---|---|
| El remuestreo elige otros frames | `generar_fixtures.py` + los dos tests de conformidad |
| Una constante cambia en un solo lado (`SCHEMA`, `T`, `IDX_MUNECA`…) | `exportar_contrato.py` + los dos tests de contrato |

En los dos casos hace falta una **referencia** que los dos lenguajes puedan
leer, y tiene que salir del código que realmente se usa: escribir a mano los
6.048 valores de `lm` de un fixture sería inviable, y copiar las constantes a un
JSON a mano reintroduce justo el error que se quiere evitar.

Estos dos scripts convierten esa referencia en algo **reproducible**: un
comando, el mismo resultado.

---

## 🔗 Qué dependencias tiene

| Dependencia | Usada por | Para qué |
|---|---|---|
| `signia_modelo.aplicacion` | `generar_fixtures` | `construir_entrada`, `indices_remuestreo` |
| `signia_modelo.dominio` | ambos | Las constantes del contrato y las entidades |
| `signia_modelo.infra.json_contrato` | `generar_fixtures` | Serializar la muestra al formato del contrato |
| `tests.factorias` | `generar_fixtures` | La mano canónica |

Reutilizar las fábricas de los tests es deliberado: **la mano de referencia debe
estar definida en un único sitio**.

`exportar_contrato.py` no depende de nada más que del módulo de constantes: es
python puro y corre en cualquier equipo, sin numpy.

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

### 🔎 Descubrimiento, no lista a mano

`exportar_contrato.py` **recorre** `dominio/contrato.py` en busca de nombres en
mayúsculas con valor serializable, en vez de enumerarlos:

```python
_NOMBRE_DE_CONSTANTE = re.compile(r"^[A-Z][A-Z0-9_]*$")
_TIPOS_EXPORTABLES = (bool, int, float, str, tuple)
```

Así una constante nueva entra en el export **sin que nadie tenga que acordarse**,
y el test de sincronía la vigila desde el primer momento. El filtro por tipo
descarta solo lo que no es un dato (`Final`, módulos, funciones).

Aparte va la lista `CLAVES_COMPARTIDAS_CON_JS`, que sí es explícita y comentada
una por una: decir *qué constantes tiene que declarar también el front* es una
decisión de diseño, no algo que se deduzca del código.

### 📐 Sin `sys.path` mágico en el paquete

El script inserta la raíz del proyecto en `sys.path` **él mismo**, para poder
ejecutarse sin instalar el paquete y sin que el paquete tenga que saber nada de
scripts.

---

## 🔍 Qué tienen los archivos

### `generar_fixtures.py`

| Función | Qué hace |
|---|---|
| `casos()` | Devuelve `{nombre: MuestraAislada}` con los seis casos límite |
| `fixture(nombre, muestra)` | Construye el dict del fixture: muestra + índices + presencia + `lm` |
| `main()` | Escribe cada fixture en `tests/fixtures/` e informa por consola |
| `CARPETA`, `DECIMALES` | Destino (`tests/fixtures`) y precisión (6) |

### `exportar_contrato.py`

| Función / constante | Qué hace |
|---|---|
| `constantes()` | Recorre `contrato.py` y devuelve `{NOMBRE: valor}` serializable |
| `contrato_exportado()` | El documento completo: `generado_por`, `version_preprocesado`, `compartidas_con_js`, `constantes` |
| `main()` | Lo escribe en `../contrato.json` con sangría de 2 (legible en un diff) |
| `CLAVES_COMPARTIDAS_CON_JS` | Las 9 constantes que el front **también** tiene que declarar, con el por qué de cada una |
| `DESTINO` | `model/contrato.json`, junto a `contrato.md`, su gemelo en prosa |

Si una clave declarada como compartida deja de existir en `contrato.py`, el
script **aborta** en vez de generar un JSON al que le falta lo que promete.

---

## 💡 Ejemplos de uso

### Regenerar los fixtures del preprocesado

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

### Regenerar el contrato exportado

```bash
venv/Scripts/python scripts/exportar_contrato.py
```

Salida:

```
contrato.json  (20 constantes)
```

Y después, **siempre**, las dos suites:

```bash
venv/Scripts/python -m pytest
cd ../front/app && pnpm test
```

> ⚠️ Regenerar solo cuando el contrato cambie **a propósito**. Hacerlo para
> "arreglar" un test en rojo esconde justo el fallo que el test existe para
> detectar: un tensor distinto entre el navegador y el entrenamiento, o una
> constante que ya no significa lo mismo en los dos lenguajes.
