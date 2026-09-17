# 📸 `componentes/captura/` — Indicadores de la grabación

## 📖 Introducción

Las tres piezas que informan de lo que está pasando mientras se graba dataset:
cuántas manos ve el detector, cuánto lleva la grabación en curso y cuántas
muestras se han guardado.

Son componentes **sin estado**: reciben un número y lo pintan.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué muestra | Dónde aparece |
|---|---|---|
| `IndicadorDeManos.jsx` | 🖐️ `sin manos` / `1 mano` / `2 manos` | Esquina superior izquierda del vídeo |
| `IndicadorDeGrabacion.jsx` | 🔴 Punto rojo pulsante + segundos transcurridos | Esquina superior derecha, solo al grabar |
| `ContadorDeMuestras.jsx` | 🔢 Número grande con las muestras tomadas | Panel derecho de Entrenamiento |

---

## 🎯 Qué problema resuelve

Grabar dataset a mano es **repetitivo y silencioso**: sin realimentación, se
acumulan decenas de muestras malas sin enterarse. Cada indicador responde a una
pregunta concreta que surge al grabar:

| Pregunta | Indicador |
|---|---|
| *¿Me está viendo la mano?* | `IndicadorDeManos` |
| *¿Estoy grabando? ¿Voy a llegar al tope de 4 s?* | `IndicadorDeGrabacion` |
| *¿Se guardó la última? ¿Cuántas llevo?* | `ContadorDeMuestras` |

El contador es además **la confirmación** de que una grabación terminó bien: si
no sube, la muestra se descartó y la línea de estado dice por qué.

---

## 🔗 Qué dependencias tiene

Ninguna más allá de React y Tailwind. No usan hooks ni conocen el dominio: los
datos llegan del hook `useCapturaSenas` a través de la página.

---

## 🧠 Cómo soluciona el problema

### 👀 Información donde se está mirando

Los dos primeros se superponen **al vídeo**, que es donde el usuario tiene los
ojos mientras hace la seña. El contador va en el panel, porque se consulta entre
grabación y grabación.

### 🔴 Un indicador que se entiende sin leer

Punto rojo + pulso: el lenguaje universal de "grabando". Los segundos con **un
decimal** bastan para ver que avanza sin que las cifras parpadeen.

### 🅰️ Plural correcto

`1 mano` / `2 manos`, y `sin manos` cuando no hay ninguna: un `0 manos` es
correcto pero se lee peor.

---

## 🔍 Qué tienen los archivos

### `IndicadorDeManos.jsx`

| Prop | Tipo | Efecto |
|---|---|---|
| `cantidad` | número | `0` → `sin manos`; `1` → `1 mano`; `2` → `2 manos` |

Fondo `bg-brand-inverso/70` con texto del color del fondo, para leerse sobre
cualquier imagen del vídeo.

### `IndicadorDeGrabacion.jsx`

| Prop | Tipo | Efecto |
|---|---|---|
| `segundos` | número | Se muestra con `DECIMALES_SEGUNDOS = 1` |

La página solo lo monta mientras `captura.grabando` es cierto.

### `ContadorDeMuestras.jsx`

| Prop | Tipo | Efecto |
|---|---|---|
| `cantidad` | número | Número grande + la etiqueta *Muestras tomadas* |

Usa `bg-secondary` con `text-brand-inverso`: es el elemento más visible del
panel, porque es el que confirma el trabajo hecho.

---

## 💡 Ejemplos de uso

```jsx
// Superpuestos al vídeo, dentro de CameraFeed
<div className="absolute inset-x-0 top-0 flex items-center justify-between gap-2 p-3 text-xs font-semibold">
    <IndicadorDeManos cantidad={captura.manosDetectadas} />
    {captura.grabando && <IndicadorDeGrabacion segundos={captura.segundos} />}
</div>
```

```jsx
// En el panel derecho
<ContadorDeMuestras cantidad={captura.muestras.length} />
```
