# 🖥️ `front/` — Interfaz web de SignIA

> Todo lo que corre en el **navegador** del usuario vive aquí.

## 🗺️ ¿Qué hay dentro?

| Carpeta | Qué es | Parte del sistema |
|---|---|---|
| [`app/`](app/) | La aplicación React + Vite | Captura de señas (Entrenamiento), traductor (futuro) y web pública |

## 🧠 Por qué el front pesa tanto en SignIA

El plan (`.claude/plan-implementacion.md`) decide que **la etapa 1 (señas → glosas) se ejecuta en el navegador** con `onnxruntime-web`: predecir ~6 veces por segundo por HTTP sería inviable. Por eso aquí hay lógica de dominio real, no solo pantallas.

## ▶️ Empezar

```bash
cd front/app
pnpm install
pnpm dev
```
