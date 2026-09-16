# 📄 `paginas/` — Pantallas del sitio

| Página | Ruta | Qué hace |
|---|---|---|
| `Inicio.jsx` | `/` | Presenta SignIA: qué es, misión y herramientas, con carrusel |
| `Traduccion.jsx` | `/traduccion` | **Modo continuo** (el producto). Deshabilitado hasta tener modelo entrenado |
| `Entrenamiento.jsx` | `/entrenamiento` | **Modo aislado**: graba muestras de una seña para el dataset |

## 🎬 Flujo de Entrenamiento

1. **Activar cámara** → aparece el vídeo con el esqueleto de la mano.
2. Escribir el **nombre de la seña**.
3. **Entrenar** → graba (vuelve a pulsar o espera 4 s) → el contador sube.
4. **Enviar** → descarga un `.json` con el lote (en la Fase 5 irá a `POST /muestras`).

Las páginas solo componen: la lógica vive en `hooks/` y las capas internas.
