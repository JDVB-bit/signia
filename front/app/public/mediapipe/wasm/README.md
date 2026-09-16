# ⚙️ `wasm/` — Runtime WebAssembly de MediaPipe

Copia literal de `node_modules/@mediapipe/tasks-vision/wasm/`. **No se edita a mano.**

| Archivo | Para qué |
|---|---|
| `vision_wasm_internal.{js,wasm}` | Runtime con SIMD (navegadores modernos) |
| `vision_wasm_module_internal.{js,wasm}` | Variante como módulo ES |
| `vision_wasm_nosimd_internal.{js,wasm}` | Respaldo para navegadores sin SIMD |

`FilesetResolver.forVisionTasks('/mediapipe/wasm')` elige la variante adecuada automáticamente.
