# 🧪 `presentacion/textos/__tests__/` — Test de la línea de estado

## 📖 Introducción

El único test de la capa de presentación, porque es la única pieza de esta capa
que es **lógica pura**: decidir qué frase ocupa la línea de estado de
Entrenamiento.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Módulo que verifica | Casos cubiertos |
|---|---|---|
| `mensajeDeEstadoDeCaptura.test.js` | `mensajeDeEstadoDeCaptura.js` | Los cinco niveles de prioridad, de arriba abajo |

El resto de la presentación son componentes: se verifican en el navegador, donde
se ve de verdad si algo está mal colocado.

---

## 🎯 Qué problema resuelve

Entrenamiento tiene **un solo renglón** para comunicarlo todo. Si la prioridad
se rompiera, el usuario vería el id de sesión justo cuando necesita leer *"La
grabación fue demasiado corta"*, y no entendería por qué el contador no subió.

Es un fallo difícil de detectar mirando: hay que provocar cada combinación. Por
eso se prueba.

---

## 🔗 Qué dependencias tiene

- `vitest` en entorno node.
- `mensajeDeEstadoDeCaptura.js` y `ESTADOS_DETECTOR`.

---

## 🧠 Cómo soluciona el problema

Cada test fija **un escalón** de la prioridad, empezando por el más fuerte:

```
aviso ▸ cámara apagada ▸ detector cargando ▸ detector con error ▸ sesión
```

Comprobar el orden completo evita el error clásico de añadir una condición nueva
al principio de la función y tapar sin querer todas las demás.

---

## 🔍 Qué tienen los archivos

| Test | Lo que garantiza |
|---|---|
| `un aviso puntual gana a todo lo demas` | Lo que acaba de pasar se lee siempre |
| `sin camara pide activarla` | La primera acción necesaria es visible |
| `informa mientras carga el detector` | El botón apagado tiene explicación |
| `informa si el detector fallo` | El error no se queda mudo |
| `con todo listo muestra la sesion` | Estado de reposo: qué tanda se está grabando |

---

## 💡 Ejemplos de uso

```bash
pnpm test -- mensajeDeEstado
```

```js
expect(
    mensajeDeEstadoDeCaptura({
        aviso: 'No se vio ninguna mano: la muestra se descartó.',
        camaraActiva: false,
        estadoDetector: ESTADOS_DETECTOR.CARGANDO,
        sesion: '2026-09-20-local',
    }),
).toBe('No se vio ninguna mano: la muestra se descartó.')   // el aviso gana
```
