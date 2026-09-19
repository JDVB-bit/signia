# 🛠️ `scripts/` — Utilidades de línea de comandos

## 📖 Introducción

Herramientas que se ejecutan a mano, fuera del paquete y fuera de los tests. Hoy
son cuatro: dos **generan la referencia compartida** con el front (los tensores
y las constantes), una **mete lo grabado en el dataset** y otra **informa de su
estado**.

Según avance el plan, aquí vivirán también el baseline DTW (Fase 3) y los
scripts de entrenamiento y exportación (Fase 4).

---

## 📂 Qué archivos tiene y qué hace cada uno

| Script | Qué hace |
|---|---|
| `generar_fixtures.py` | 🔁 Regenera `tests/fixtures/*.json`: las muestras límite y el tensor que produce Python |
| `exportar_contrato.py` | 📜 Regenera `../contrato.json`: las constantes de `dominio/contrato.py` en formato legible por JS |
| `inspeccionar.py` | 🔬 Informe del dataset crudo y dibujo de una trayectoria. Es la **puerta de la Fase 2** |
| `importar_lote.py` | 📥 Mete en el dataset los ficheros que descarga el botón *Enviar* del front |

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

`inspeccionar.py` resuelve otro problema: **saber si el dataset que se está
grabando sirve**. Descubrir al entrenar que una clase tiene la mitad de muestras
que las demás, que todo salió de una sola sesión o que MediaPipe perdió la mano
en el 40 % de los frames cuesta una tarde de regrabación — y a veces volver a
convocar a la gente.

---

## 🔗 Qué dependencias tiene

| Dependencia | Usada por | Para qué |
|---|---|---|
| `signia_modelo.aplicacion` | `generar_fixtures` | `construir_entrada`, `indices_remuestreo` |
| `signia_modelo.dominio` | ambos | Las constantes del contrato y las entidades |
| `signia_modelo.infra.json_contrato` | `generar_fixtures` | Serializar la muestra al formato del contrato |
| `tests.factorias` | `generar_fixtures` | La mano canónica |
| `signia_modelo.aplicacion.inspeccion` | `inspeccionar` | Resumir, diagnosticar y sacar la trayectoria |
| `signia_modelo.aplicacion.importacion_de_lote` | `importar_lote` | El caso de uso que tambien usa `POST /muestras` |
| `signia_modelo.infra.json_lote` | `importar_lote` | Validar el sobre que descarga el front |
| `signia_modelo.infra` | `inspeccionar` | Repositorio en disco, informe de texto y lienzo ASCII |

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

### 🔁 El script y el endpoint son el mismo caso de uso

`importar_lote.py` no reimplementa nada: llama a `muestras_desde_lote()` y a
`importar_lote()`, que es exactamente lo que hace `POST /muestras` en el
backend. Por eso importar a mano y pulsar *Enviar* no pueden acabar guardando
cosas distintas.

Valida **todos** los ficheros antes de escribir **ninguno**: importar a medias
dejaria el dataset en un estado que nadie recuerda, y habria que ir a buscar
cuales entraron.

### 🚪 El inspector es una puerta, no un visor

`inspeccionar.py` **devuelve código de salida 1** si queda algún aviso
bloqueante. Así el mismo comando que se mira a ojo mientras se graba sirve de
puerta automática cuando haya CI, sin escribir el criterio dos veces.

Con `--etiqueta` la vista es parcial, así que los criterios globales se
desactivan (y lo dice en el informe): afirmar *"falta reposo"* mirando solo
`hola` sería un falso bloqueo.

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

### `inspeccionar.py`

| Opción | Qué hace |
|---|---|
| `--datos RUTA` | Raíz del dataset (por defecto, `DATOS_DIR` o `./data`) |
| `--etiqueta SENA` | Limita las tablas a una clase y acota el diagnóstico |
| `--trayectoria SENA` | Dibuja el recorrido de la muñeca de una muestra |
| `--muestra N` | Cuál dibujar, en el orden alfabético de los ficheros |
| `--lado izquierda\|derecha` | Qué mano dibujar (por defecto, la que más aparece) |

| Función | Qué hace |
|---|---|
| `imprimir_informe(repo, etiqueta)` | Resume, diagnostica, imprime y dice si hay bloqueos |
| `imprimir_trayectoria(repo, etiqueta, posicion, lado)` | Carga esa muestra y la dibuja |
| `main()` | Orquesta y traduce `ErrorDeContrato` en un mensaje accionable |

### `importar_lote.py`

| Opcion | Que hace |
|---|---|
| `ficheros...` | Uno o varios lotes `.json` descargados del front |
| `--datos RUTA` | Raiz del dataset (por defecto, `DATOS_DIR` o `./data`) |
| `--seco` | Valida y cuenta, pero no escribe nada |

| Funcion | Que hace |
|---|---|
| `leer_lote(ruta)` | Un fichero -> muestras ya validadas |
| `leer_todos(rutas)` | Todas las muestras y todos los errores, antes de escribir |
| `main()` | Importa e informa por etiqueta; devuelve 1 si algo era invalido |

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

### Inspeccionar el dataset

```bash
venv/Scripts/python scripts/inspeccionar.py
```

Salida (con un dataset a medio grabar):

```
Dataset SignIA en C:\...\model\data

Senas aisladas (entrenamiento): 3 clases, 84 muestras, 2 sesiones
  clase        muestras sesiones  frames segundos con mano 2 manos
  hola               32        2    30.0     1.00      99%       0
  reposo             40        2    30.9     1.03       0%       0
  tu                 12        2    30.6     1.02     100%       0

Frases completas (evaluacion, nunca entrenan)
  frases: 6 | secuencias distintas: 2 | glosas por frase: 2.5 | sesiones: 1
  glosario usado: hola, tu

Diagnostico (6 avisos)
  [BLOQUEA ] 'tu' tiene 12 muestras; hacen falta 30.
  [BLOQUEA ] 'reposo' tiene 40 muestras y deberia tener 64 (el doble de la clase mas poblada): es el separador entre senas.
  [BLOQUEA ] Hay 6 frases completas; hacen falta 20 para medir WER.
  [atencion] hola #32 tiene 6 frames; por debajo de 12 el remuestreo repite cada frame y la muestra queda casi estatica.
  [atencion] hola #32 solo tiene mano detectada en el 17% de los frames (minimo 50%).
  [atencion] Solo hay 2 secuencias distintas y se esperaban 3: repetir la misma frase no mide la segmentacion.
```

Y para mirar una muestra concreta con los ojos:

```bash
venv/Scripts/python scripts/inspeccionar.py --trayectoria hola --muestra 5
```

```
Trayectoria de la muneca derecha en 2026-09-20-snt-01-0004.json
30 frames, mano presente en 30. tiempo: . inicio -> @ final
+------------------------------------------------+
|                          #@                    |
|                        *#                      |
|                      +*                        |
|                   ==+                          |
|                 --=                            |
|               :-                               |
|             .:                                 |
|            .                                   |
+------------------------------------------------+
```

El gradiente de caracteres cuenta el tiempo (`.` primero, `@` último), así que
se ve **hacia dónde** iba la mano y no solo la forma del trazo.

### Importar lo grabado

```bash
venv/Scripts/python scripts/importar_lote.py ~/Descargas/signia-hola-2026-09-20-local.json
```

Salida:

```
Leyendo 1 fichero(s):
  signia-hola-2026-09-20-local.json: 4 muestras

Importadas 4 muestras en C:\...\model\data
  hola: +3
  reposo: +1

Siguiente paso: python scripts/inspeccionar.py
```

Y si un fichero no cumple el contrato, no entra nada:

```
  ERROR malo.json: muestra 0 del lote: falta la lista 'frames'
No se importo nada: corrige los ficheros invalidos.
```

> 💡 Con el backend levantado este paso sobra: el boton *Enviar* del front sube
> el lote a `POST /muestras`, que ejecuta este mismo caso de uso. El script
> sigue siendo util para los ficheros de respaldo que se descargan cuando el
> backend no responde.
