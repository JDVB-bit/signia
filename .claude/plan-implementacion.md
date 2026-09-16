# Plan de implementación — SignIA

> Escrito en la sesión 34, reestructurado en la 37 alrededor del objetivo real:
> **traducir frases, no palabras sueltas.**
> Cubre **sólo desarrollo**; el despliegue es una fase aparte y deliberadamente
> posterior (ver §Independencia del despliegue).
> Rol: Snt escribe el código; Claude guía, revisa y hace los estilos Tailwind.

---

## Objetivo del producto

**El usuario hace una frase seguida en LSE delante de la cámara y SignIA la
transcribe entera.** Eso es un traductor. Reconocer una seña por pulsación sería
un diccionario inteligente, y no es el producto.

## Arquitectura en dos etapas (leer antes que nada)

SignIA **no es un modelo**, son dos etapas con responsabilidades separadas:

```
vídeo ──► ETAPA 1: reconocimiento          ──► ETAPA 2: redacción      ──► texto
          nuestro modelo (PyTorch/ONNX)         agente de texto (LLM)
          señas ──► secuencia de GLOSAS         glosas ──► español natural
          ["hola","como","estar","tu"]          "Hola, ¿cómo estás?"
```

- **Etapa 1 (nuestro modelo):** clasifica **señas individuales** y emite la
  secuencia de palabras reconocidas, en el orden en que se hicieron. Eso es todo
  lo que hace. Su salida son **glosas**: palabras sueltas, sin conjugar, sin
  artículos, sin puntuación — el orden de LSE, no el del español.
- **Etapa 2 (otro agente):** convierte esa secuencia de glosas en una frase
  natural en español. Es un problema de **texto**, no de visión, y se resuelve
  con un LLM (Fase 6b).

### La unidad de aprendizaje es la SEÑA, nunca la frase

Esto es lo que hace que el sistema funcione con frases que nadie ha grabado:

- Con `n` señas aprendidas, el sistema puede transcribir **cualquier combinación
  y cualquier orden** de esas `n` señas. Aprendes 20 señas y obtienes
  prácticamente infinitas frases.
- Si la unidad de aprendizaje fuera la frase, el sistema sólo conocería las
  frases grabadas, y no se puede predecir cómo va a hablar alguien. Sería
  inviable, y Snt tiene razón en señalarlo.

**Por tanto: se entrena SIEMPRE con muestras de una sola seña.** Las frases que
se graban en la Fase 2c **no entrenan el clasificador**: se usan para medir y
para calibrar el segmentador. Está detallado ahí mismo, con el por qué.

### Tres consecuencias del objetivo que no son obvias

1. **La inferencia de la etapa 1 corre en el navegador**, no en el backend. El
   modo continuo predice ~6 veces por segundo; una petición HTTP por ventana es
   insostenible. La etapa 2, en cambio, es **una llamada por frase** y sí va al
   backend (donde vive la clave del LLM).
2. **Hay que grabar frases completas** además de señas aisladas — para **medir y
   calibrar**, no para entrenar. Sin frases de test no se sabe si el sistema
   traduce; con ellas se ajustan los umbrales del segmentador.
3. **Dos métricas separadas, y no hay que mezclarlas:** **WER sobre las glosas**
   mide nuestro modelo (etapa 1); la calidad del español final mide la etapa 2.
   Si se juntan, un texto malo se le echa en cara al modelo o al revés, y no se
   arregla ninguno de los dos.

### Dos modos, y por qué existen los dos

| | Modo aislado | Modo continuo |
|---|---|---|
| Para qué | **Capturar dato etiquetado** para entrenar | **El producto**: traducir |
| Quién lo usa | Snt / colaboradores, en `Entrenamiento` | El usuario final, en `Traduccion` |
| Ventana | explícita (pulsas Entrenar) | deslizante, automática |
| Unidad | una seña | una seña por ventana, encadenadas |
| Fases | 1-2 | 6 + 6b |

No compiten: el aislado es el **camino de entrenamiento**, el continuo es el
**camino de inferencia**. No se puede entrenar sin el primero ni entregar sin el
segundo.

### Alcance del vocabulario

**Abierto: `n` señas.** No hay ningún número de clases escrito en el código:
`n` se deriva del dataset al entrenar. Empezar con pocas señas es una decisión
de *datos*, no de arquitectura (ver §Escalar a `n` señas).

### Entrada

Manos (`HandLandmarker`, ya integrado). La expresión facial y la posición
respecto al cuerpo también son portadoras de significado en LSE; se mitiga
parcialmente conservando la posición de la muñeca en el encuadre (Fase 0), y
`PoseLandmarker` es la ampliación natural (ver decisión en Fase 2).

---

## Principios de diseño (no negociables)

1. **Los landmarks CRUDOS son la fuente de verdad.** Se guardan tal como los
   devuelve MediaPipe, sin normalizar. Features, pesos y métricas son derivados
   y reconstruibles. Cambiar el preprocesado o `T` obliga a reentrenar, nunca a
   regrabar.
2. **El preprocesado existe una sola vez.** Como ahora hay inferencia en JS y
   entrenamiento en Python, "una sola vez" se consigue metiendo la normalización
   **dentro del grafo ONNX** (ver Fase 0). Es la única forma de que no divergan;
   dos implementaciones a mano divergen siempre, y el bug es silencioso.
3. **El entrenamiento es un job por lotes, nunca un paso de gradiente en un
   request.** Se reentrena desde cero con todo el dataset.
4. **Un modelo nuevo no reemplaza al activo si sus métricas son peores.**
5. **La capa de persistencia va detrás de una interfaz.** Nada de rutas
   absolutas ni SDK de nube en la lógica de dominio.
6. **El modelo aprende señas, nunca frases.** La unidad de una muestra de
   entrenamiento es siempre una sola seña. Las frases se graban para evaluar y
   calibrar; convertir la secuencia de glosas en español natural es trabajo de
   la etapa 2, fuera del modelo.
7. **La métrica que manda es el WER sobre glosas**, no la accuracy por muestra
   — y se mide separada de la calidad del texto final.

---

## Fase 0 — Contrato de datos

**Objetivo:** fijar el formato de una muestra. Es la decisión más difícil de
revertir: cambiarla invalida lo ya grabado.

### Ficheros
- `model/contrato.md` — el contrato en prosa (fuente de verdad).
- `model/preprocess.py` — remuestreo temporal (Python, para entrenar).
- `model/normalizacion.py` — las operaciones que se exportan **dentro del ONNX**.

### Formato de transporte y almacenamiento (CRUDO)

```json
{
  "schema": 1,
  "etiqueta": "hola",
  "sesion": "2026-09-20-snt-01",
  "fps_aprox": 30,
  "frames": [
    {
      "t": 0,
      "manos": [
        { "lado": "derecha", "score": 0.98,
          "lm": [[0.1, 0.2, 0.0], "... 21 puntos ..."] }
      ]
    }
  ]
}
```

- `lado` viene del *handedness* de MediaPipe, **no** del orden de detección.
- Ojo: el vídeo se muestra espejado en `CameraFeed`, pero el `lado` se refiere a
  la mano real. **Verificar empíricamente en la Fase 1, antes de grabar nada.**
- Un frame puede tener 0, 1 o 2 manos. No se rellena: la ausencia es información.
- `sesion` identifica la tanda de grabación. Imprescindible para la evaluación
  honesta de la Fase 4.

### Features derivadas (lo que ve el modelo)

Longitud fija `T = 48` frames (≈1.6 s), remuestreo por interpolación lineal.
Por mano (dos ranuras fijas: izquierda, derecha):

| Bloque | Valores | Por qué |
|---|---|---|
| presencia | 1 | 0/1, distingue "mano ausente" de "mano en el origen" |
| posición de muñeca | 2 | `x,y` en el encuadre — conserva *dónde* se hace la seña |
| escala | 1 | distancia muñeca → nudillo medio, proxy de profundidad |
| forma | 60 | los 20 landmarks restantes, relativos a la muñeca y divididos por la escala |

**64 por mano → F = 128 features por frame. Tensor de entrada: (48, 128).**

La forma es invariante a traslación y escala (da igual dónde estés y a qué
distancia), pero la posición y la escala se conservan aparte como señal útil.

### El reparto entre JS y el grafo ONNX

Esto resuelve el principio 2 y es la decisión técnica central de la fase:

```
JS / Python (idéntico y trivial):  elegir 48 índices de frames  → (48, 2, 21, 3) + presencia
Dentro del grafo ONNX:             restar muñeca, calcular escala, dividir, concatenar → (48, 128)
                                   → Encoder → Cabeza → logits
```

Sólo el remuestreo (aritmética de índices, ~10 líneas) se escribe dos veces; toda
la normalización vive en el grafo, así que es literalmente el mismo código en
entrenamiento y en el navegador.

### Test de conformidad (obligatorio)
`model/tests/fixtures/` con N muestras crudas y sus tensores esperados generados
por Python. Un test en JS (`front/app/src/lib/__tests__/`) comprueba que el
remuestreo JS coincide con el de Python a 1e-5. Es la red que impide la deriva.

### Decisiones tomadas
- [x] **`T = 48` confirmado por Snt.** Si en la Fase 2 se mide que las señas
      duran sistemáticamente más de ~1.6 s se revisa, pero como el crudo se
      guarda sin recortar, cambiar `T` sólo obliga a reentrenar.
- [x] **Ventana de grabación explícita: se graba cuando el usuario pulsa
      "Entrenar"** (pulsar para iniciar, pulsar de nuevo o límite de tiempo para
      terminar). Sin autodetección en el modo de captura.

**Hecho cuando:** existe el remuestreo en Python, la normalización como módulo
exportable a ONNX, y el test de conformidad pasa con 0, 1 y 2 manos y con
secuencias más cortas y más largas que 48 frames.

---

## Fase 1 — Captura en el front (sin backend)

**Objetivo:** cerrar el bucle cámara → landmarks → muestra en disco local, sin
haber escrito una línea de API.

### Ficheros
- `front/app/src/lib/useCapturaSenas.js` — hook nuevo.
- `front/app/src/utils/CameraFeed.jsx` — extender para exponer el `<video>`.
- `front/app/src/pages/Entrenamiento.jsx` — conectar botones.

### Qué hace el hook
- `requestAnimationFrame` sobre el `<video>` → `detectForVideo()` del
  `HandLandmarker` ya existente.
- Buffer de frames mientras graba.
- API: `{ grabando, alternarGrabacion, muestras, borrarUltima, exportar }`.
- Las muestras se acumulan en memoria del navegador; no se envían todavía.

### Semántica de los botones
- **Entrenar** → captura una muestra: pulsar inicia la grabación, pulsar otra vez
  (o alcanzar el tope de duración) la cierra. Incrementa "Muestras tomadas".
- **Enviar** → en esta fase descarga un `.json` con todas las muestras
  acumuladas. En la Fase 6 pasará a llamar al endpoint.

### Pendiente de esta fase
- [ ] Feedback visual mientras graba (borde de la cámara en `secondary`,
      contador de segundos) — Claude hace los estilos.
- [ ] **Overlay del esqueleto de la mano sobre el vídeo** (canvas). Muy
      recomendado: permite descartar muestras malas antes de guardarlas, y en la
      Fase 2 vas a grabar cientos.
- [ ] **Verificar el handedness con el vídeo espejado.** Si el `lado` que reporta
      MediaPipe está invertido respecto a lo que ves y lo descubres con 300
      muestras grabadas, hay que parchear o regrabar el dataset entero.

**Hecho cuando:** se graban 3 muestras seguidas, el contador sube a 3, y "Enviar"
descarga un JSON con 3 secuencias de landmarks plausibles.

---

## Fase 2 — Dataset

**Objetivo:** tener datos. Sin esto todo lo demás es teoría. Y para un traductor
hacen falta **dos tipos** de dato, no uno.

### 2a. Señas aisladas (para entrenar el clasificador)
- El vocabulario inicial que decidas + una clase **`reposo`**.
- **Recomendación:** empezar con 5-10 señas. No por límite de la arquitectura
  (soporta `n`), sino para llegar rápido al bucle completo con datos de calidad.
- **30-40 muestras por clase.**
- Variar deliberadamente: luz, distancia, posición en el encuadre, velocidad,
  ropa, fondo. Si consigues que otras personas graben, el salto de calidad es
  enorme — un dataset de una sola persona produce un modelo que sólo funciona
  contigo, y es el mayor riesgo del proyecto.
- Grabar en **sesiones separadas e identificadas** (`sesion`).

### 2b. La clase `reposo`, en serio
En el modo continuo `reposo` no es una clase más: **es el segmentador**, lo que
marca la frontera entre una seña y la siguiente. Necesita más dato y más variedad
que las demás:
- manos bajadas, quieto;
- manos en el encuadre sin hacer nada;
- **frames de transición** entre dos señas (la mano yendo de una postura a otra).
  Estos son los que más fallan y los que nadie graba.
- Sugerencia: 2-3× más muestras que una seña normal.

### 2c. Frases completas — conjunto de EVALUACIÓN, no de entrenamiento

> ⚠️ **Estas frases NO entrenan el clasificador.** El modelo se entrena
> exclusivamente con las muestras de una sola seña de 2a/2b. Si se entrenara con
> frases como unidad, el sistema sólo conocería las frases grabadas y no habría
> forma de anticipar cómo se va a expresar alguien. La generalización a frases
> nuevas viene de que la unidad aprendida es la seña; el resto es composición.

Grabar vídeos de **frases seguidas**, etiquetadas con la *secuencia* de glosas:

```json
{ "schema": 1, "tipo": "frase", "etiquetas": ["hola", "como", "estas"],
  "sesion": "...", "frames": [ ... ] }
```

Sirven para tres cosas, todas imprescindibles y ninguna es entrenar:
1. **Medir WER** (Fase 4) — sin frases de test no sabes si el sistema traduce o
   sólo clasifica clips recortados a mano.
2. **Calibrar el segmentador** de la Fase 6 (cuántas ventanas seguidas hacen
   falta para emitir, qué confianza mínima). Esos números no se adivinan; salen
   de barrerlos contra estas frases y quedarse con el mejor WER.
3. **Habilitar el roadmap v2 (CTC)** — ver la nota de esa sección: CTC tampoco
   memoriza frases, aprende la *alineación* entre vídeo y secuencia de glosas.
   Grabar esto ahora es casi gratis; añadirlo después significa volver a convocar
   a todo el mundo.

**Cantidad mínima:** 20-30 frases, en al menos 2 sesiones distintas, combinando
las señas del vocabulario en **órdenes variados** — incluidas combinaciones que
no tengan sentido gramatical. Lo que se mide es la segmentación y el
reconocimiento, no la frase.

### Ficheros
- `model/data/crudo/aisladas/<etiqueta>/*.json` — ignorado en git.
- `model/data/crudo/frases/*.json` — ignorado en git.
- `model/scripts/inspeccionar.py` — muestras por clase, duración media, frames
  sin manos, plot de una trayectoria para ver que tiene sentido.

### Decisión pendiente
- [ ] **¿Grabar también `PoseLandmarker` desde el principio?** Es la única
      decisión irreversible de esta fase: el crudo es la fuente de verdad, y lo
      que no grabes hoy no lo podrás usar mañana sin regrabar. Si la meta a medio
      plazo es vocabulario grande (100+), grábalo aunque el modelo v1 lo ignore.

**Hecho cuando:** `inspeccionar.py` reporta ≥30 muestras por clase, `reposo`
sobrerrepresentada, ≥20 frases completas, y ninguna anomalía obvia.

---

## Fase 3 — Baseline sin entrenamiento (DTW + k-NN)

**Objetivo:** responder "¿son mis datos separables?" antes de culpar al modelo.
Media tarde de trabajo que te ahorra días depurando una red que nunca podía
funcionar.

### Ficheros
- `model/baseline_dtw.py`

DTW entre secuencias remuestreadas + vecino más cercano, evaluado con
*leave-one-session-out*. Imprime accuracy y matriz de confusión.

**Hecho cuando:** hay un número escrito. Si da >85%, los datos son buenos. Si da
cerca del azar (1/n_clases), el problema está en la captura o en el
preprocesado, no en el modelo — vuelve a la Fase 0/1/2.

---

## Fase 4 — Modelo y evaluación

**Objetivo:** el clasificador, su pipeline reproducible, y — lo más importante —
la medición a nivel de frase.

### Ficheros
- `model/dataset.py` — `Dataset` de PyTorch: lee crudo, remuestrea, augmenta.
- `model/model.py` — `Encoder` + `Cabeza` + la normalización del grafo.
- `model/train.py` — entrenamiento + evaluación + artefacto.
- `model/evaluar_frases.py` — **el harness de WER**.
- `model/config.py` — hiperparámetros en un solo sitio.
- `model/exportar_onnx.py`

### Arquitectura de partida

Tres piezas **separadas** (ver §Escalar a `n` señas para el por qué de la última):

```
Normalización: (48, 2, 21, 3) + presencia → (48, 128)     [va dentro del ONNX]
Encoder:       (B, 48, 128) → GRU(hidden=128, layers=2, dropout=0.3) → (B, 128)
Cabeza:        (B, 128) → Linear(128 → n_clases)
```

`n_clases` se deriva de las etiquetas del dataset al arrancar el entrenamiento;
no aparece escrito en ninguna parte. ~130k parámetros, y la cabeza crece de forma
trivial con el vocabulario (128 × n).

Alternativas si el GRU sobreajusta: 1D-CNN / TCN (a menudo mejor con datasets
diminutos y más rápida). Con vocabularios grandes, un *Transformer* pequeño.

### Augmentación (obligatoria con este volumen de dato)
Ruido gaussiano en los landmarks, escalado temporal (±20%), espejo
izquierda↔derecha, rotación pequeña en el plano, *dropout* de frames.

### Evaluación en dos niveles

**Nivel 1 — por muestra aislada.** Split **por sesión de grabación, nunca
aleatorio** (con split aleatorio, dos frames de la misma grabación caen en train
y test y tu accuracy es ficción). Reportar accuracy global, accuracy por clase,
matriz de confusión, curva de pérdida.

**Nivel 2 — por frase, sobre la secuencia de GLOSAS (la que manda).**
`evaluar_frases.py` toma las frases de la Fase 2c, corre el pipeline continuo
completo (ventana deslizante + consolidación, la misma lógica de la Fase 6) y
compara la secuencia de glosas emitida contra la de referencia con **WER**:

```
WER = (sustituciones + inserciones + borrados) / palabras de referencia
```

Reportar además, desglosado, porque cada error se arregla distinto:
- **inserciones** → palabras fantasma: umbral de confianza o `reposo` demasiado débil;
- **borrados** → señas que se pierden: ventana mal dimensionada o `k` demasiado alto;
- **sustituciones** → confusión real entre clases: problema del modelo o del dato.

Esta separación es la que convierte "no funciona" en una acción concreta.

**La etapa 2 no se evalúa aquí.** El WER mide nuestro modelo con glosas crudas;
la calidad del español final se juzga aparte (Fase 6b). Mezclarlas impide saber
cuál de las dos está fallando.

**Este script también es el que calibra los umbrales:** barre `k` y el umbral de
confianza sobre las frases de la Fase 2c, se queda con la combinación de mejor
WER, y la escribe en `umbrales.json` dentro del artefacto.

### Artefacto de salida

```
model/artefactos/v1/
  weights.onnx     con la normalización incluida en el grafo
  labels.json      índice → nombre de seña (orden canónico por id estable)
  umbrales.json    confianza mínima, k de consolidación — calibrados, no adivinados
  manifest.json    schema, T, F, preprocess_version, accuracy, WER, fecha, nº muestras
```

**Hecho cuando:** `train.py` produce el artefacto completo, `exportar_onnx.py`
verifica que la salida del ONNX coincide con la de PyTorch a 1e-4 (no es
opcional: ahí aparecen los bugs de exportación), y `evaluar_frases.py` imprime un
WER con su desglose.

---

## Fase 5 — Backend

**Objetivo:** recoger dato, entrenar, y **servir el artefacto**. Ojo: el backend
ya no está en el camino crítico de la traducción.

### Estructura

```
back/app/
  main.py
  api/
    muestras.py         POST /muestras
    modelos.py          GET /modelos/activo  (manifest + URL del .onnx)
    prediccion.py       POST /predecir   (una ventana — sólo depuración)
    entrenamientos.py   (Fase 7)
  dominio/
    esquemas.py         Pydantic: valida el crudo del contrato
    repositorio.py      INTERFAZ abstracta
  infra/
    repo_local.py       SQLite + ficheros en disco
    registro_modelos.py modelo activo, versiones, rollback
  config.py             todo por variables de entorno, defaults locales
```

`model/` se consume como paquete (`pip install -e`): el backend **no**
reimplementa nada del preprocesado. La API sirve con `onnxruntime`, no con torch.

### Endpoints

| Método | Ruta | Para qué |
|---|---|---|
| `POST` | `/muestras` | lote de muestras crudas (aisladas o frases) |
| `GET` | `/modelos/activo` | manifest + etiquetas + umbrales + URL del `.onnx` |
| `GET` | `/modelos/activo/weights.onnx` | el artefacto, estático y cacheable |
| `POST` | `/predecir` | una ventana → etiqueta. **Sólo depuración**, no el producto |
| `POST` | `/redactar` | glosas → español natural (etapa 2, Fase 6b) |
| `GET` | `/salud` | versión del modelo, nº de clases, versión de preprocesado |

### Modelo de datos (SQLite)

```
muestras        id, tipo(aislada|frase), etiqueta, etiquetas_json, ruta,
                n_frames, schema, origen, sesion, estado, creado_en
senas           id, etiqueta, descripcion            ← orden canónico de clases
entrenamientos  id, estado, creado_en, terminado_en, modelo_version,
                metricas_json, error
modelos         version, ruta, accuracy, wer, preprocess_version, activo, creado_en
```

Las secuencias **no** van dentro de la DB: van como ficheros y la fila guarda la
`ruta`. `estado` permite descartar una muestra mala sin borrarla.

**Hecho cuando:** `POST /muestras` persiste, `GET /modelos/activo` devuelve un
manifest válido, y el `.onnx` se descarga por HTTP.

---

## Fase 6 — Reconocimiento continuo → secuencia de glosas (etapa 1)

**Objetivo:** el usuario hace una frase seguida y salen las glosas en orden.
Esta fase **no** produce español natural: produce `["hola","como","estar","tu"]`.
La redacción es la Fase 6b.

### Por qué en el navegador
El modo continuo predice cada ~5 frames, unas 6 veces por segundo. Una petición
HTTP por ventana sería insostenible en latencia, coste y batería. Por tanto el
modelo se descarga una vez (`GET /modelos/activo/weights.onnx`) y se ejecuta con
**`onnxruntime-web`**. Consecuencias, todas buenas: latencia cero, coste de
servidor cero, funciona sin conexión tras la primera carga, y el backend deja de
ser el cuello de botella. A cambio, los pesos viajan al cliente — irrelevante en
este proyecto.

### Ficheros
- `front/app/src/lib/modeloOnnx.js` — carga el `.onnx` + `labels` + `umbrales`,
  cachea en IndexedDB, comprueba versión contra `/modelos/activo`.
- `front/app/src/lib/useReconocimientoContinuo.js` — el hook del pipeline.
- `front/app/src/pages/Traduccion.jsx` — UI de transcripción en vivo.

### El pipeline de consolidación

```
frames ──► buffer de 48 ──► cada ~5 frames: remuestreo + inferencia ──► logits
                                                                          │
                                                                          ▼
                                            probabilidad máxima < umbral ──► descartar
                                                                          │
                                            etiqueta == reposo ──► cerrar palabra, rearmar
                                                                          │
                                            misma etiqueta k ventanas ──► EMITIR palabra
                                                                          │
                                                                          ▼
                                                                    transcripción
```

Reglas que evitan los dos fallos clásicos:
- **No repetir**: una palabra emitida no se vuelve a emitir hasta pasar por
  `reposo`. Sin esto sale "hola hola hola hola" mientras la mano está quieta.
- **Umbral de confianza**: si nada supera el umbral, no se emite nada. Una
  transcripción incompleta es mejor que una inventada.
- `k` y el umbral vienen de `umbrales.json`, **calibrados** con las frases de la
  Fase 2c. No los pongas a ojo.

### UI
- **Traducir** pasa a ser un interruptor: arranca/detiene una sesión de
  traducción en vivo. No es un botón por seña.
- La caja que ya existe en `Traduccion.jsx` se convierte en una **tira de glosas
  que crece** palabra a palabra, con la glosa en curso marcada de otro modo.
- Indicador de estado: escuchando / seña detectada / reposo.
- Botón de limpiar. Claude hace los estilos.
- En la Fase 6b esta tira se mantiene visible (es la evidencia de lo que el
  modelo reconoció) y debajo aparece el texto redactado.

### Limitación honesta, y hay que asumirla
Este enfoque exige **pausas mínimas entre señas**. El señado natural y fluido
—con coarticulación, señas que se solapan y `reposo` que desaparece— no lo
resuelve una ventana deslizante. Para la demo: frase a ritmo moderado con micro-
pausas. La solución real es el roadmap v2.

**Hecho cuando:** se hace la frase objetivo seguida delante de la cámara y
aparecen las glosas en orden, sin repeticiones ni palabras fantasma, con un WER
medido en el harness de la Fase 4 coherente con lo que se ve.

---

## Fase 6b — Redacción: glosas → español natural (etapa 2)

**Objetivo:** convertir `["hola","como","estar","tu"]` en "Hola, ¿cómo estás?".

Esto **no es cosmético**. LSE tiene gramática propia: orden distinto del español,
verbos sin conjugar, sin artículos, sin preposiciones, la interrogación marcada
con la cara y no con signos. Pasar de glosas a español es una traducción real
entre dos lenguas, y es un problema de **texto**. Nuestro modelo de visión no
tiene por qué saber nada de eso.

### Por qué un LLM y no reglas
- **Reglas/plantillas:** sólo funcionan con un conjunto cerrado de frases
  previstas. Vuelve a aparecer el problema de "no se puede predecir cómo hablará
  alguien". Sirve como *fallback* sin conexión, no como solución.
- **Seq2seq propio:** haría falta un corpus paralelo glosa→español que no
  tenemos. Fuera de alcance.
- **LLM (recomendado):** generaliza a cualquier combinación, añade puntuación,
  conjuga, resuelve la interrogación. Una llamada por frase, coste despreciable
  al volumen de este proyecto.

### Dónde corre: en el backend, obligatoriamente
La clave de API **no puede estar en el navegador**. Así que:

```
navegador: glosas ──► POST /redactar ──► backend ──► LLM ──► texto ──► navegador
```

Es **una llamada por frase**, no por ventana, así que no hay problema de coste ni
de latencia. Nótese el reparto que queda: la etapa 1 (6/s) nunca sale del
navegador; la etapa 2 (1 por frase) sí va al servidor.

### Endpoint
`POST /redactar` → `{ glosas: ["hola","como","estar","tu"] }` → `{ texto: "..." }`

Tres guardas, y la primera no es opcional:
- **Validar cada glosa contra la tabla `senas` antes de construir el prompt.**
  Si se acepta texto arbitrario, se abre la puerta a inyección de prompt. Como el
  vocabulario es cerrado, validar contra el conjunto de etiquetas la cierra por
  completo.
- **Instrucción anti-invención:** el LLM redacta *sólo* con lo que hay en las
  glosas; no añade contenido. Temperatura baja.
- **Fallback:** si el backend o el LLM no responden, mostrar la tira de glosas
  tal cual. Degradado, pero el producto sigue siendo usable.

### Ficheros
- `back/app/api/redaccion.py` — el endpoint.
- `back/app/infra/llm.py` — el cliente; `LLM_API_KEY` por variable de entorno.
- `back/app/dominio/prompt.py` — el prompt: vocabulario disponible, explicación
  de que la entrada son glosas de LSE, y el formato de salida esperado.
- `front/app/src/pages/Traduccion.jsx` — pintar glosas y texto redactado.

### Cuándo se dispara
Al cerrar la frase: cuando el usuario detiene la sesión, o tras un `reposo`
prolongado (~2 s). No en cada palabra — redactar a medias produce texto que se
reescribe solo delante del usuario y se ve mal.

### Evaluación
Cualitativa, sobre las frases de la Fase 2c: pasar las glosas **de referencia**
(no las predichas) por la etapa 2 y juzgar el español resultante. Usar las de
referencia es lo que aísla esta etapa de los errores de la etapa 1.

**Hecho cuando:** se hace la frase objetivo delante de la cámara y aparecen las
dos cosas: la tira de glosas reconocidas y, debajo, la frase en español bien
formada.

---

## Fase 7 — Reentrenamiento en caliente

- `POST /entrenamientos` → valida (mínimo de muestras por clase, ningún job en
  curso) → crea el job → responde `202 { job_id }`.
- Worker: `BackgroundTasks` + lock en la DB es suficiente a esta escala.
- **Compara métricas contra el modelo activo — y compara el WER, no sólo la
  accuracy.** Si empeora, no promociona. Escribe el artefacto en temporal y hace
  `rename` atómico.
- `GET /entrenamientos/{id}` → estado, métricas, error.
- El front detecta la nueva versión en `/modelos/activo`, descarga el `.onnx` y
  recarga la sesión sin recargar la página.
- Rollback: `POST /modelos/{version}/activar`.

**Decisión pendiente:** ¿el botón **Enviar** dispara el reentrenamiento?
- **Opción A (recomendada):** sí. `POST /muestras` devuelve `job_id`, el front
  hace poll. El bucle completo se ve en la demo.
- **Opción B:** no. Acción de administración aparte, endpoint protegido, sin UI.
  Más seguro, menos vistoso.

**Ojo:** este es el único punto donde el servidor necesita torch. La alternativa
es exportar el dataset, entrenar en el PC de Snt con CUDA y subir el artefacto.
Se decide en el despliegue, **no** ahora: el código es el mismo.

---

## Fase 8 — Robustez antes de exponerlo

- **Auth** en `/muestras` y `/entrenamientos` (token por cabecera). Abiertos a
  internet permiten envenenar el dataset y disparar entrenamientos.
- **Límites:** tamaño de payload, nº máximo de frames, *rate limit* simple.
- `estado = "pendiente"` por defecto para muestras de origen desconocido; sólo
  entrenan las `aprobada`.
- `model/scripts/backup.py` — el dataset crudo es el activo irreemplazable.
- Logs de cada sesión de traducción (palabras emitidas, confianzas, versión) para
  detectar degradación.

---

## Roadmap v2 — del umbral a CTC

La ventana deslizante es un heurístico: funciona con pausas, se rompe con señado
fluido. La solución de libro es entrenar el modelo directamente sobre frases
completas con **pérdida CTC** (*Connectionist Temporal Classification*), que
aprende la alineación entre el vídeo y la secuencia de glosas sin que nadie le
diga dónde empieza cada seña. Es exactamente el mismo mecanismo que usa el
reconocimiento de voz.

> **Aclaración importante, porque suena a lo contrario de lo que dice el
> principio 6:** CTC **tampoco memoriza frases.** Su alfabeto de salida es el
> vocabulario de señas, y lo que aprende de una frase es *dónde* está cada seña
> dentro del vídeo, no la frase como unidad. Sigue generalizando a combinaciones
> y órdenes que nunca vio; sólo cambia de qué aprende la segmentación: en la v1
> la segmenta un heurístico calibrado a mano, en la v2 la aprende el modelo.

Qué hace falta: muchas más frases etiquetadas (cientos, no 20) y un decodificador
*beam search* en inferencia. Nada de la Fase 0-5 se tira: mismo contrato, mismo
preprocesado, mismo encoder — cambian la cabeza y la pérdida.

**Por eso la Fase 2c graba frases desde el principio.** Es la inversión más
barata del plan: hoy cuesta una tarde, y es lo que hace que la v2 sea una
evolución en vez de empezar de cero.

---

## Escalar a `n` señas

Lo que cambia con la escala **no es el modelo**.

### Lo que hay que hacer bien desde el día 1 (barato)
- **`n` se deriva del dataset, nunca se escribe.** `Linear(128 → n_clases)` con
  `n_clases = len(labels)`. Ningún número de clases en el código, el front o la API.
- **Las etiquetas son datos con id estable.** La tabla `senas` da el orden
  canónico (por id, no por inserción ni alfabético) y `labels.json` viaja
  **dentro** del artefacto. Si el orden cambia entre entrenamientos, los
  artefactos viejos quedan mal interpretados y el rollback deja de funcionar.
- **Cabeza desacoplada del encoder**, para poder cambiar softmax → prototipos.

### El muro real es el dato

| Vocabulario | Muestras (~30/clase) | Horas de grabación | Viable |
|---|---|---|---|
| 10 señas | 300 | ~2 h | sí |
| 50 señas | 1.500 | ~8 h | sí, con esfuerzo |
| 500 señas | 15.000 | ~60-80 h | no, grabando tú solo |
| 1000 señas | 30.000 | ~125-150 h | requiere colaboradores o dataset externo |

A partir de ~100 señas aparecen dos problemas que el número de clases no
anticipa:
1. **Sólo manos deja de bastar** — muchas señas se diferencian por expresión
   facial o por dónde se hacen respecto al cuerpo. Toca `PoseLandmarker` (y de
   ahí la decisión pendiente de la Fase 2).
2. **El reentrenamiento completo deja de ser instantáneo** — con 30.000 muestras
   el job pasa de segundos a minutos u horas, y el bucle "Enviar → reentrena → ya
   la reconoce" se rompe.

### La salida a escala: encoder + prototipos
Con vocabulario grande la arquitectura correcta pasa de clasificador a **métrica**:
un encoder entrenado con *triplet/contrastive loss*, y cada seña representada por
el promedio de sus muestras (su "prototipo") guardado en la DB.

- Dar de alta la seña nº 501 = grabar 10 muestras, calcular el prototipo,
  insertarlo. **Sin reentrenar, en un segundo, sin olvido.**
- El encoder se reentrena en frío de vez en cuando, pero no hace falta para
  añadir señas.
- Es la idea original de Snt ("el modelo aprende la seña nueva") bien
  implementada, y la razón de separar `Encoder` y `Cabeza` desde hoy.

**Recomendación:** softmax para el primer tramo (decenas de señas, donde es más
preciso y más simple de entender), con el código preparado para sustituir la
cabeza. No implementar prototipos ahora: sin dataset, un encoder métrico no tiene
de qué aprender.

---

## Independencia del despliegue

Reglas que hacen que el despliegue sea una decisión posterior y barata:

1. Toda configuración por **variables de entorno** con defaults que funcionan en
   local (`DATOS_DIR=./data`, `DB_URL=sqlite:///./data/signia.db`,
   `VITE_API_URL`).
2. `dominio/repositorio.py` es una **interfaz**. Cambiar de SQLite+disco a
   Firestore+GCS es escribir una segunda implementación, sin tocar endpoints.
3. **Cero SDK de nube** importado fuera de `infra/`.
4. Ninguna ruta absoluta ni supuesto de "el fichero sigue ahí" en el dominio.
5. `docker-compose.yml` local que arranca back + volumen.

Ventaja añadida de tener la etapa 1 en el navegador: el backend sólo se toca para
enviar muestras, entrenar y **redactar**. Si se cae, el reconocimiento de glosas
sigue funcionando y sólo se pierde el español pulido (fallback: mostrar las
glosas). La demo no se rompe.

**La clave del LLM (`LLM_API_KEY`) vive únicamente en el backend**, por variable
de entorno, y nunca se expone al front ni se versiona. Es el único secreto real
del proyecto.

---

## Orden y dependencias

```
Fase 0 (contrato) ──► Fase 1 (captura) ──► Fase 2 (dataset: aisladas + reposo + FRASES)
                                                          │
                                                          ▼
                                                   Fase 3 (baseline DTW)
                                                          │
                                                          ▼
                                            Fase 4 (modelo + WER por frase)
                                                          │
                                        ┌─────────────────┴─────────────────┐
                                        ▼                                   ▼
                              Fase 5 (backend)                  Fase 6 (glosas en vivo) ─┐
                                        │                                   │            │
                                        │                                   ▼            │
                                        │                         Fase 6b (redacción)◄───┘
                                        │                                   │
                                        └─────────────────┬─────────────────┘
                                                          ▼
                                        Fase 7 (reentrenar) ──► Fase 8 (robustez) ──► despliegue
                                                          │
                                                          ▼
                                                    v2: CTC
```

La Fase 6b depende del backend (Fase 5) por la clave del LLM, pero la Fase 6 no:
se puede tener el reconocimiento de glosas funcionando en el navegador con el
`.onnx` leído de un fichero estático, sin servidor ninguno.

Las fases 0-4 **no necesitan backend ni servidor**: puedes tener un modelo
entrenado y un WER medido antes de escribir un endpoint. Y como la inferencia
corre en el navegador, la Fase 6 tampoco depende de la 5 más que para descargar
el artefacto — en desarrollo puede leerlo de un fichero estático.

---

## Riesgos principales

| Riesgo | Mitigación |
|---|---|
| Dataset de una sola persona → modelo que sólo funciona con Snt | Grabar con otras personas; augmentación agresiva; evaluar por sesión |
| Sobreajuste con 40 muestras/clase | Modelo pequeño, dropout, augmentación, *early stopping* |
| **Señado fluido en modo continuo** | Ventana deslizante + `reposo` exige micro-pausas; asumirlo en la demo y planificar CTC como v2 |
| **`reposo` mal grabada arruina la segmentación** | Sobrerrepresentarla e incluir frames de transición entre señas (Fase 2b) |
| **Buena accuracy aislada pero transcripción basura** | Medir WER desde la Fase 4, no sólo accuracy; desglosar inserciones/borrados/sustituciones |
| Deriva entre el preprocesado de JS y el de Python | Normalización dentro del grafo ONNX + test de conformidad con fixtures |
| Sin cara/torso, señas ambiguas | Vocabulario inicial discriminable sólo con manos; decidir en Fase 2 si se graba `PoseLandmarker` |
| Cambiar el preprocesado invalida el trabajo | Se guarda crudo: se cambia y se reentrena, sin regrabar |
| Handedness invertido por el espejo del vídeo | Verificar empíricamente en la Fase 1, antes de grabar el dataset |
| Vocabulario grande sin dato suficiente | El muro son las horas de grabación; crecer por tramos y medir en cada uno |
| Orden de clases inestable entre artefactos | `labels.json` dentro del artefacto + orden canónico por id en `senas` |
| **Confundir las dos etapas al diagnosticar** | WER sobre glosas mide el modelo; el español final se juzga aparte pasando glosas de referencia (Fase 6b) |
| **El LLM "rellena" y se inventa contenido que no se señó** | Instrucción anti-invención + temperatura baja + la tira de glosas siempre visible junto al texto, como evidencia |
| **Inyección de prompt vía las glosas** | Validar cada glosa contra la tabla `senas` antes de construir el prompt; vocabulario cerrado = superficie cerrada |
| Dependencia de un servicio externo para la etapa 2 | Fallback a mostrar las glosas crudas; el reconocimiento no depende del LLM |
