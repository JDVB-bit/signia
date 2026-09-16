# 🪝 `hooks/` — Estado y efectos de React

Cada hook tiene una responsabilidad; los grandes **componen** a los pequeños.

## 📸 Captura de muestras

```
useCapturaSenas
 ├─ useDetectorDeManos      carga MediaPipe y expone su estado
 ├─ useBucleDeDeteccion     requestAnimationFrame → detectForVideo por frame nuevo
 ├─ useGrabacionDeMuestra   iniciar / acumular / cerrar / abortar una grabación
 └─ useMuestrasCapturadas   lote de muestras en memoria
```

## 🧰 Generales

| Hook | Responsabilidad |
|---|---|
| `useCamara` | Permiso, flujo de la cámara y apagado al desmontar |
| `useTema` | Tema claro/oscuro sincronizado con el documento |
| `useIntroInicial` | Mostrar la intro solo en la primera visita |
| `useCerrarConEscape` | Cerrar menús y diálogos con Escape |

## 💡 Uso

```jsx
const captura = useCapturaSenas({ videoRef, canvasRef, etiqueta: 'hola', activo: camaraActiva })
captura.alternarGrabacion()   // empieza / termina una muestra
captura.exportar()            // descarga el lote como JSON
```
