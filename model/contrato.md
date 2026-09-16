# Contrato de datos — SignIA (Fase 0)

> **Fuente de verdad.** El codigo de `signia_modelo/` implementa este documento;
> si los dos discrepan, manda este documento y el codigo esta mal.
> Version del formato: `schema = 1`. Version del preprocesado: `1`.

Cambiar algo de aqui **no invalida el dataset ya grabado** (se guarda crudo),
pero **s� obliga a reentrenar** y a tocar el remuestreo de JS a la vez.

---

## 1. Formato de transporte y almacenamiento (CRUDO)

Lo que el front env�a y lo que se guarda en disco. Son los landmarks tal como
los devuelve MediaPipe: **sin normalizar, sin recortar, sin rellenar**.

```json
{
  "schema": 1,
  "tipo": "aislada",
  "etiqueta": "hola",
  "sesion": "2026-09-20-snt-01",
  "fps_aprox": 30,
  "frames": [
    { "t": 0,
      "manos": [
        { "lado": "derecha", "score": 0.98, "lm": [[0.1, 0.2, 0.0], "...21 puntos..."] }
      ]
    }
  ]
}
```

| Campo | Obligatorio | Notas |
|---|---|---|
| `schema` | s� | debe valer `1`; cualquier otro valor se rechaza |
| `tipo` | no | `"aislada"` (por defecto) o `"frase"` |
| `etiqueta` | en aisladas | una sola glosa |
| `etiquetas` | en frases | secuencia de glosas en orden |
| `sesion` | s� | identifica la tanda de grabaci�n; sin esto la evaluaci�n de la Fase 4 es falsa |
| `fps_aprox` | no | informativo |
| `frames[].t` | no | �ndice del frame; por defecto su posici�n |
| `frames[].manos` | no | 0, 1 o 2 manos. **La ausencia no se rellena: es informaci�n** |
| `manos[].lado` | s� | `"izquierda"` / `"derecha"`, del *handedness* de MediaPipe |
| `manos[].score` | no | `[0, 1]`, por defecto `1.0` |
| `manos[].lm` | s� | exactamente 21 puntos de 3 coordenadas |

**Ojo con el espejo:** el v�deo se muestra espejado en pantalla, pero `lado` se
refiere a la mano **real**. Hay que verificarlo emp�ricamente en la Fase 1,
antes de grabar el dataset.

**Dos manos con el mismo `lado`:** MediaPipe puede equivocarse. Regla �nica en
todo el proyecto: gana la de mayor `score`; a igualdad, la primera. Implementada
en `Frame.mano()` y en ning�n otro sitio.

### Muestras aisladas y frases

- **Aislada** = una sola se�a. **Es la �nica unidad de entrenamiento.**
- **Frase** = varias se�as seguidas. **Nunca entrena**: sirve para medir WER y
  para calibrar los umbrales del segmentador (plan, Fase 2c).

### En disco

```
<DATOS_DIR>/crudo/aisladas/<etiqueta>/<sesion>-<n>.json
<DATOS_DIR>/crudo/frases/<sesion>-<n>.json
```

`DATOS_DIR` es una variable de entorno (por defecto `./data`). La etiqueta y la
sesi�n se sanean antes de usarse como ruta: vienen del usuario.

---

## 2. Remuestreo temporal (la �nica pieza duplicada en JS)

De `n` frames grabados a `T = 48` fijos (~1.6 s a 30 fps).

```
indice(i) = int( i * (n - 1) / (T - 1) + 0.5 )     para i = 0 .. T-1
```

- Se **eligen** frames, no se interpolan. Interpolar entre un frame con mano y
  otro sin ella inventar�a medias manos que MediaPipe nunca produjo.
- Si sobran frames se saltan; si faltan se repiten. Los extremos siempre se
  conservan (`indice(0) = 0`, `indice(T-1) = n-1`).
- El redondeo se escribe `int(x + 0.5)` **a prop�sito**: `round()` de Python
  redondea al par (`round(0.5) == 0`) y `Math.round` de JS no (`1`). Con
  `round()` el navegador y el entrenamiento ver�an tensores distintos, y el fallo
  ser�a silencioso.
- JS debe calcular en el mismo orden: `Math.round(i * ((n - 1) / (T - 1)))`.

**Test de conformidad:** `tests/fixtures/*.json` contiene muestras crudas y el
tensor que produce Python. El test de JS lee esos mismos ficheros y compara a
`1e-5`. Regenerar con `python scripts/generar_fixtures.py`.

---

## 3. Tensor crudo (salida de Python, entrada del grafo)

```
lm        (T, 2, 21, 3)  float32   landmarks crudos
presencia (T, 2)         float32   1.0 si esa mano est� en el frame, 0.0 si no
```

- Ranuras **fijas y can�nicas**: `0 = izquierda`, `1 = derecha`. Nunca el orden
  de detecci�n.
- Mano ausente: `lm` en ceros **y** `presencia = 0`. Eso distingue "no hay mano"
  de "hay una mano en el origen".

---

## 4. Features (dentro del grafo ONNX)

La normalizaci�n **no se ejecuta en Python en producci�n**: viaja dentro del
`.onnx`, para que el navegador y el entrenamiento ejecuten literalmente el mismo
c�digo. Por mano, 64 valores en este orden exacto:

| Offset | Valores | Bloque | Por qu� |
|---|---|---|---|
| 0 | 1 | presencia | distingue ausencia de origen |
| 1 | 2 | posici�n de la mu�eca (`x`, `y`) | en LSE *d�nde* se hace la se�a es significado |
| 3 | 1 | escala: distancia mu�eca -> nudillo medio (landmark 9), en el plano `x,y` | proxy de profundidad |
| 4 | 60 | forma: los 20 landmarks restantes menos la mu�eca, divididos por la escala | invariante a traslaci�n y a escala |

`F = 64 x 2 = 128`. **Tensor de entrada del modelo: `(48, 128)`**, ranura
izquierda primero.

Reglas de borde:
- La escala se *clampa* a `1e-6` antes de dividir: una mano degenerada no puede
  producir `NaN` dentro del grafo.
- Todo el bloque se multiplica por la presencia: la mano ausente sale en **ceros
  exactos**, pase lo que pase con su relleno.
- La `z` de MediaPipe entra en la forma pero **no** en la escala ni en la
  posici�n: es una profundidad relativa demasiado ruidosa para normalizar con
  ella.

---

## 5. Reparto JS / ONNX

```
JS y Python (id�ntico y trivial):  elegir 48 �ndices -> (48,2,21,3) + presencia
Dentro del grafo ONNX:             restar mu�eca, escala, dividir, concatenar -> (48,128)
                                   -> Encoder -> Cabeza -> logits
```

Nombres de entrada/salida del grafo: `lm`, `presencia` -> `features`. Ejes
din�micos: lote y tiempo (compartidos por las dos entradas).

---

## 6. Qu� rompe qu�

| Cambio | Hay que regrabar | Hay que reentrenar | Hay que tocar JS |
|---|---|---|---|
| `T`, features, normalizaci�n | no | **s�** | s�, si cambia el remuestreo |
| A�adir una se�a al vocabulario | no | s� | no |
| Formato JSON (`schema`) | no, pero hay que migrar los ficheros | s� | s� |
| A�adir `PoseLandmarker` | **s�** | s� | s� |

Lo �nico irreversible es **no grabar** algo. Por eso el crudo se guarda entero.
