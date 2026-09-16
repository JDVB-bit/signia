# 🧩 `src/` — Código fuente del front

Organizado con **Clean Architecture**: cada capa solo conoce a las de dentro.

| Capa | Carpeta | Depende de | Ejemplo |
|---|---|---|---|
| 🎯 Dominio | [`dominio/`](dominio/) | nada | contrato de datos, reglas de grabación |
| ⚙️ Aplicación | [`aplicacion/`](aplicacion/) | dominio | remuestreo, crear una muestra |
| 🔌 Infraestructura | [`infra/`](infra/) | dominio | MediaPipe, canvas, localStorage, cámara |
| 🎨 Presentación | [`presentacion/`](presentacion/) | todas | páginas, componentes y hooks de React |
| 🖼️ Recursos | [`assets/`](assets/) | — | imágenes que importan los componentes |

## 📄 Archivos sueltos

| Archivo | Para qué sirve |
|---|---|
| `main.jsx` | Punto de entrada: aplica el tema antes de pintar, monta el router y `AplicacionRaiz` |
| `index.css` | Tailwind + la paleta de 5 colores (clara y oscura) como variables |

## 🧪 Tests

Cada capa con lógica tiene su carpeta `__tests__/` al lado del código:

```bash
pnpm test                       # todos
pnpm test -- aplicacion         # solo los de una capa
```

## ✅ Regla práctica al añadir código

1. ¿Es una regla del negocio sin dependencias? → `dominio/`
2. ¿Orquesta reglas para un caso de uso? → `aplicacion/`
3. ¿Habla con una API del navegador o una librería externa? → `infra/`
4. ¿Es React? → `presentacion/`
