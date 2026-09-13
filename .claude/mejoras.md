# Lista de mejoras, implementaciones y sugerencias — SignIA

> Lista viva según la regla 3 de `.claude/claude.md`. Se actualiza en cada sesión.

## Hecho
- [x] Paleta de colores principal (brand/bg/surface/secondary) como CSS vars de Tailwind v4 en `front/app/src/index.css`.
- [x] Paleta oscura calculada por color complementario (matiz +180°) + luminosidad invertida.
- [x] Botón `ThemeToggle` con persistencia en `localStorage` y detección de preferencia del sistema.
- [x] `App.jsx` migrado a las clases de la nueva paleta.

## Hecho (sesión 2)
- [x] `BurgerMenu.jsx` — botón hamburguesa animado a X, panel con overlay, cierre con click fuera / Escape / al elegir un enlace, foco en el primer enlace al abrir.
- [x] Aplicado en `App.jsx` (sustituyendo el botón `*toolbar` placeholder) y en `Traduccion.jsx` (que no tenía cabecera con estilos ni `ThemeToggle`).

## Hecho (sesión 3)
- [x] Botones del header (`ThemeToggle`, `BurgerMenu`) sin caja/contorno; usan `text-secondary` / `bg-secondary` solo en los elementos internos (emoji, barras).
- [x] `App.jsx`: título "Traductor de lenguaje..." centrado y más grande (`text-3xl`/`sm:text-4xl`).
- [x] Layout responsivo en grid: sección "Que es?" (con la burbuja de información dentro) a la izquierda, sección reservada para imágenes/animaciones a la derecha; en móvil se apilan verticalmente.

## Hecho (sesión 4)
- [x] Layout mucho más ancho (`max-w-[110rem]`), secciones con más padding, mejor aprovechamiento de los bordes de pantalla.
- [x] Título principal más grande e imponente (`text-4xl`→`lg:text-6xl`, `font-extrabold`, `drop-shadow-sm`).
- [x] Animación de aparición "polvo" (`animate-dust-in` en `App.css`) aplicada palabra por palabra al título, con retraso escalonado.
- [x] Componente `Typewriter.jsx` — animación de escritura simple, usado en el párrafo de "Que es?".
- [x] Borrador de contenido para "Que es?" (descripción, herramientas, misión, autoría académica) en `.informacion-homepage.md`, ignorado en git — pendiente de que Snt lo corrobore antes de llevarlo al código.

## Hecho (sesión 5)
- [x] Expandido `.informacion-homepage.md`: contenido organizado en 3 secciones (Que es / Mision / Herramientas), cada una con texto **Breve** (tarjeta) y **Detalle** (burbuja de información propia por sección).

## Hecho (sesión 6)
- [x] `.informacion-homepage.md`: los textos "Breve" de las 3 secciones se ampliaron a párrafos generales que ocupan la tarjeta (ya no titulares de una línea); "Detalle" sigue siendo lo específico para la burbuja.

## Hecho (sesión 7)
- [x] `.informacion-homepage.md`: reescrito en punto medio de longitud y limpiado de todo detalle técnico (sin React, MediaPipe, PyTorch, FastAPI, "landmarks", frontend/backend); todo redactado en términos de experiencia de usuario.

## Hecho (sesión 8)
- [x] Contenido de `.informacion-homepage.md` aplicado a `App.jsx`: 3 secciones reales (Que es / Mision / Herramientas), cada una con su texto breve (con animación de escritura) y su propia burbuja de información.
- [x] `InfoBubble.jsx` — nuevo componente: la burbuja de información ahora despliega un panel dinámico (overlay + cierre con click fuera/Escape/botón ✕) para mejor lectura del detalle, en vez del placeholder de botón.
- [x] `SectionCard.jsx` — pequeño componente de tarjeta reutilizado por las 3 secciones.
- [x] Corregido bug: el título con efecto "polvo" perdía los espacios entre palabras (el `inline-block` recortaba el espacio final); ahora el espacio va como nodo de texto fuera del `span`.

## Hecho (sesión 9)
- [x] Corregido el título "Que es?" → "¿Qué es?" (tilde y signo de apertura).
- [x] Layout reordenado: "¿Qué es?" queda siempre junto a la sección de imágenes (fila 1, 2 columnas). Misión y Herramientas pasaron a una fila aparte, en 12 columnas (7/5) con Herramientas desplazada hacia abajo (`lg:mt-16`) y padding distinto, para que no se sienta como una grilla uniforme.
- [x] `InfoBubble.jsx` — ahora es un modal centrado en pantalla (`fixed inset-0 flex items-center justify-center`), con `backdrop-blur-sm` sobre el fondo, texto más grande (`text-lg`), interlineado amplio (`leading-loose`) y letras espaciadas (`tracking-wide`). Verificado por estilos computados (blur(8px), 18px, 36px de interlineado).
- [x] `SectionCard.jsx` acepta ahora `className` para variar tamaño/padding por sección.

## Hecho (sesión 10)
- [x] Quitado el desfase vertical (`lg:mt-16`) entre Misión y Herramientas; ahora tienen el mismo alto (verificado: 284px ambas, mismo `top`), manteniendo el ancho distinto (7/5 columnas).

## Hecho (sesión 11)
- [x] Animación de entrada del modal de `InfoBubble`: desciende desde arriba (`translateY(-32px)→0`), 500ms exactos con curva `cubic-bezier(0.16,1,0.3,1)` — verificado con `getAnimations()` que la duración es 500ms, dentro del límite pedido.
- [x] `CarouselImage.jsx` — componente que recibe la imagen por prop (`src`/`alt`) y solo se encarga de pintarla; separa "qué imagen mostrar" de "cómo animar el cinturón".
- [x] `ImageBelt.jsx` — efecto cinturón: cada imagen visible ~5s, la siguiente empuja a la anterior hacia la izquierda con transición fluida (700ms), loop infinito sin salto (clon de la primera imagen al final del cinturón + reset invisible).
- [x] 3 imágenes de `front/app/src/assets` (`senas-persona1/2/3.jpg`) integradas en el cinturón, reemplazando el placeholder de la sección de imágenes.

## Hecho (sesión 12)
- [x] Sección de imágenes reducida (`h-56`/`sm:h-64`, `max-w-md`) y centrada verticalmente respecto a la tarjeta "¿Qué es?" (`items-center` en el grid de la fila 1, en vez de estirarse a la misma altura).
- Nota: Snt ajustó por su cuenta los tiempos de animación (`dust-in` a 1500ms, `modal-drop-in` a 2000ms, `TIEMPO_VISIBLE_MS` del carrusel a 7500ms) — no se tocó nada de eso.

## Hecho (sesión 13)
- [x] Confirmado: no habrá cuarta imagen por ahora (se queda en 3).
- [x] Verificado el layout en móvil: con `grid-cols-1` (por debajo de `lg`), "¿Qué es?" ya queda arriba y la imagen debajo, centrada y en su tamaño reducido (224px de alto) — no hizo falta tocar código, ya se comportaba así.

## Hecho (sesión 14) — Pantalla de carga (intro)
- [x] `IntroSplash.jsx` + `IntroSplash.css` (componente aparte, en `utils/`): pantalla de carga con fondo `color-brand`, título "SignIA" + lema apareciendo centrados y grandes, luego "succionados" (2.8s, curva de aceleración) hasta la posición/tamaño aproximados del header real, con un crossfade final de color/fondo hacia los tonos reales de la app antes de desmontarse. Duración total ≈4.65s, bajo el límite de 6s.
- [x] Barra de carga con una mano-emoji que se desliza y cambia de "seña" (🖐️→🤟→🤙→👌) a los cortes de 25/75/99% del progreso — alternativa vía CSS/emoji ya que no hay assets de manos, tal como se autorizó.
- [x] `AppRoot.jsx` — orquestador nuevo: mientras la intro está activa, `App` ni se monta (así ninguna otra animación de la página corre en paralelo); al terminar (`onFinish`), guarda `signia-intro-vista=1` en `localStorage` y monta `App`. Un reload posterior ya no vuelve a mostrar la intro (verificado).
- [x] `utils/theme.js` — se extrajo la lógica de tema (antes solo en `ThemeToggle`) para aplicarse de forma sincrónica en `main.jsx` ANTES de montar React, evitando parpadeos de tema tanto en la intro como en la app real (verificado en claro y oscuro).
- [x] No se tocó ninguno de los tiempos/valores que Snt ajustó por su cuenta (`App.css`, `ImageBelt.jsx`).

## Hecho (sesión 15)
- [x] Quitada la regla de "no volver a salir si recargas": ahora **toda** carga muestra algo.
- [x] `IntroSplash.jsx` acepta `soloFade`: si ya se vio la animación completa antes (`localStorage`), no se repite — solo se ve el mismo fondo `color-brand` desvaneciéndose (500ms) hasta dejar ver la home, que ya está montada detrás.
- [x] `AppRoot.jsx` reestructurado: primera vez = animación completa sin montar `App` (regla 4 intacta); cualquier otra vez = `App` se monta de una vez y el velo rápido se superpone encima. Verificado ambos casos en el navegador (primera carga con animación completa, recarga con solo el velo).

## Hecho (sesión 16)
- [x] Revertido el velo de recarga (`soloFade`): la intro vuelve a ser exactamente "una sola vez, punto" — `AppRoot.jsx` e `IntroSplash.jsx`/`.css` de vuelta a como estaban antes de esa prueba.
- [x] Verificada la paleta: todo (incluida la intro) usa `var(--color-brand/bg/surface/secondary)`, así que ya refleja los valores actuales del disco sin necesidad de tocar nada.
- [x] Trabajo de frontend dividido en 4 commits en `main`:
  1. `d2067f2` chore: retirar scaffold antiguo `front/signia`.
  2. `f97eb25` feat: botones del header (`ThemeToggle`, `BurgerMenu`, `theme.js`).
  3. `557bd66` feat: estructura del proyecto, secciones y contenido de la home.
  4. `14e168c` feat: pantalla de carga inicial (animación).
- Nota: quedaron sin commitear (fuera del alcance de "frontend"): `.claude/launch.json`, `.gitignore` (raíz), `.claude/claude.md`, `.claude/mejoras.md` — pendiente de que Snt diga si quiere versionarlos.

## Hecho (sesión 17) — bug de color en la intro
- [x] `IntroSplash.css`: el fondo del overlay usaba `--color-brand`; se cambió a `--color-bg` (el fondo real del sitio). El título usa `--color-brand` desde el inicio (ya no blanco + crossfade), y la barra de carga pasó de blanco fijo a `--color-brand`/`--color-secondary` — todo coherente con la paleta activa. Verificado en claro y oscuro con estilos computados.

## Hecho (sesión 18)
- [x] `.claude/` agregado al tracking de git y commiteado (`760de5d`): `claude.md`, `mejoras.md`, `launch.json` actualizado.
- [x] `Header.jsx` — header común extraído (título+lema, tema, burger menu), usado ahora en `App.jsx` y en las páginas nuevas, para que sea idéntico en todo el sitio en vez de copiado.
- [x] `pages/Traduccion.jsx` y `pages/Entrenamiento.jsx` — estructura básica (header + fondo `bg-bg`) con su título de sección; contenido específico de cada una queda pendiente.
- [x] `BurgerMenu`: agregado el enlace a "Entrenamiento" junto a Inicio y Traductor.
- Todo esto en el commit `ddc4484`.

## Hecho (sesión 19)
- [x] Instalado `react-router-dom` y conectadas las 3 páginas de verdad: `BrowserRouter` en `main.jsx`, `Routes`/`Route` en `AppRoot.jsx` (`/`, `/traduccion`, `/entrenamiento`), y `BurgerMenu` usando `<Link>` en vez de `<a>` planos. Verificado navegando por el menú y recargando directo en `/traduccion` (fallback SPA de Vite).
- [x] Confirmado (por historial de git) que no se tocó la paleta de colores en ningún commit propio; solo se corrigió a qué variable apuntaba la intro.

## Hecho (sesión 20)
- [x] `PageLayout.jsx` — nuevo componente base en `utils/`: agrupa el wrapper comun a toda pagina de SignIA (div raiz `min-h-screen bg-bg...` + `<Header/>` + `<main className="mx-auto max-w-[110rem]...">`), recibiendo el contenido de cada pagina como `children` (asi cada una mantiene libertad sobre su propio titulo, incluido el efecto "polvo" de la home).
- [x] `App.jsx` migrado a `PageLayout` como base. Verificado en el navegador (screenshot + sin errores de consola/servidor): la home se ve identica a como estaba antes del cambio.

## Hecho (sesión 21)
- [x] `pages/Traduccion.jsx` y `pages/Entrenamiento.jsx` migradas a `PageLayout.jsx` (ya las tres paginas comparten la misma base). Verificado navegando a `/traduccion` y `/entrenamiento` en el navegador: identicas a como estaban antes, sin errores.

## Hecho (sesión 22)
- [x] `CameraFeed.jsx` — nuevo componente reutilizable en `utils/`: rectangulo que pide `getUserMedia({video:true})` y muestra el video en vivo (espejado por defecto). Estados: inicial (boton "Activar camara"), solicitando, activa, denegada y no-soportada, cada uno con su mensaje.
- [x] Guarda en `localStorage` (`signia-camera-permiso`, "concedido"/"denegado") si el usuario ya habia dado el permiso antes; si es asi, en la siguiente visita activa la camara sola en vez de mostrar el boton (el permiso real lo sigue controlando el navegador, esto es solo para no pedirle de nuevo un clic de mas).
- [x] Integrado en `pages/Entrenamiento.jsx` dentro de una seccion `aspect-video`. Verificado en el navegador: rectangulo con boton "Activar camara"; al hacer clic pasa a estado "denegada" (la vista previa embebida bloquea camara real) y lo guarda en localStorage; forzando `signia-camera-permiso=concedido` en localStorage y recargando, confirma que intenta activar la camara automaticamente sin clic. Sin errores de consola propios del componente.

## Hecho (sesión 23)
- [x] `CameraFeed.jsx`: cambiado `localStorage` → `sessionStorage` para recordar el permiso de camara. Decidido con Snt tras evaluar el trade-off: `sessionStorage` dura solo mientras la pestaña este abierta (sobrevive recargas y alternar entre paginas en la misma visita, pero se olvida solo al cerrar la pestaña), a diferencia de `localStorage` (para siempre) o una variable de JS en memoria (ni siquiera sobrevive una recarga). Asi se evita mostrar el boton de nuevo al alternar Entrenamiento/Traduccion en una misma visita, sin arrastrar el permiso "recordado" a una visita futura.
- [x] Verificado en el navegador: con `sessionStorage` vacio se muestra el boton; forzando `signia-camera-permiso=concedido` en `sessionStorage` y navegando a Entrenamiento, intenta activar la camara sola (bloqueado por la vista previa embebida, comportamiento esperado) y actualiza `sessionStorage` a "denegado"; `localStorage` se confirma en `null` en todo momento (ya no se usa). Sin errores de consola propios del componente.
- [x] Componente `CameraFeed` dado por terminado por ahora, a la espera de las siguientes instrucciones de Snt.

## Hecho (sesión 24)
- [x] `Button.jsx`: agregada la variante `secondary` (vacia, como el resto — sin estilos definitivos todavia) para poder distinguir semanticamente los botones principal/secundario aunque hoy se vean iguales (nativos, sin clase).
- [x] `pages/Entrenamiento.jsx`: nueva seccion de controles del pipeline, debajo de la camara — input controlado con label "Nombre seña", contador de "Muestras tomadas" (state en 0, a la espera del pipeline real de captura), y los botones `Entrenar` (`variant="primary"`) y `Enviar` (`variant="secondary"`) usando el componente `Button` existente. Los handlers (`handleEntrenar`/`handleEnviar`) quedan como TODO, sin logica real todavia.
- [x] Verificado en el navegador: el input recibe texto, ambos botones son clickeables (via accesibilidad, `ref_5`/`ref_6`), sin errores de consola propios.

## Hecho (sesión 25) — diseño de Entrenamiento
- [x] `index.css`: agregadas `--color-brand-inverso` y `--color-secondary-inverso`. Cada una vale el `brand`/`secondary` de la paleta CONTRARIA al tema activo (definidas al reves entre `@theme` y `.dark`, mismo mecanismo que el resto de la paleta), para que ciertos elementos resalten siempre con el color "del otro tema" sin importar cual este puesto.
- [x] `Button.jsx`: variantes `primary` (`bg-brand-inverso`, texto blanco) y `secondary` (`bg-secondary-inverso`, texto oscuro) ya con estilos reales — antes estaban vacias.
- [x] `pages/Entrenamiento.jsx` rediseñada: camara a la izquierda con ~15-18% de margen respecto al borde del contenido (columna vacia `lg:w-[15%]`) y los controles (nombre de seña, contador, botones) a la derecha, cada bloque a 35% del ancho; en pantallas chicas (`<lg`) se apila todo verticalmente sin el margen. Contador de muestras convertido en una insignia tipo boton (`bg-brand-inverso`, numero grande centrado, `rounded-2xl`).
- [x] Verificado en el navegador en ambos temas: en claro, contador/Entrenar usan el azul-gris de la paleta oscura y Enviar el beige claro de la paleta oscura; en oscuro se invierte (naranja/gris claro) — confirmado tambien por posiciones/anchos exactos via `getBoundingClientRect` (margen izquierdo ~18.5% del contenido, cada bloque 35%). Sin errores de consola propios.

## Hecho (sesión 26) — ajustes de Snt sobre el diseño anterior
- [x] Snt ajusto a mano `index.css` (`--color-secondary-inverso`) y probo un `color-brand` (clase invalida) en el contador de `Entrenamiento.jsx` — no se revirtio nada de eso, se tomo como base.
- [x] Arreglada la tipografia de `Button.jsx` (`primary`/`secondary`) y del contador: el FONDO sigue usando el color inverso (paleta contraria, sin tocar), pero el TEXTO ahora usa `text-brand` (el color de tipografia del tema ACTUAL, no el inverso) en vez del `text-white`/`text-slate-900`/`color-brand` (invalido) que habia antes.
- [x] `pages/Entrenamiento.jsx`: camara reubicada al 30% izquierdo de la pagina y los controles al 30% derecho (antes 35%/35%), con margenes/espacio de 10%/20%/10% repartidos entre medio. Verificado con `getBoundingClientRect` (30.0%/30.0% exactos) y los colores de texto/fondo con `getComputedStyle` en ambos temas.
- Nota para Snt: el 30% pedido es MENOR al 35% anterior — technically no hace la camara "mas grande" en ancho. Se aplico el numero tal cual lo diste; avisame si en realidad querias un porcentaje mayor.
- Nota: no se toco `index.css` (`--color-secondary-inverso`) mas alla de lo que Snt ya habia dejado — en modo oscuro ese valor (`#F5EBD0`) es en realidad el `--color-bg` de la paleta clara, no su `--color-secondary` (`#C0CAD1`); posible descuido a confirmar con Snt si fue a proposito.

## Hecho (sesión 27) — desacoplar el texto de los botones del brand general
- [x] Bug reportado por Snt: al modificar `--color-brand` (pensado solo para titulos/tipografia general), el texto de los botones/contador cambiaba tambien, porque ambos usaban la misma variable (`text-brand`).
- [x] `index.css`: agregada `--color-brand-texto`, copia independiente de `--color-brand` (mismo valor hoy en ambos temas) pensada especificamente para texto sobre fondos `*-inverso`. Ahora tocar el `brand` de titulos no mueve el texto de los botones, y viceversa.
- [x] `Button.jsx` (`primary`/`secondary`) y el contador de `pages/Entrenamiento.jsx`: cambiado `text-brand` → `text-brand-texto`.
- [x] Verificado en el navegador: se forzo `--color-brand` a un color de prueba (magenta) en runtime y se confirmo que el titulo cambiaba pero el texto del boton NO — quedaron desacoplados. Colores visuales sin cambios respecto a antes, en ambos temas.

## Hecho (sesión 28) — simplificado a 5 colores + grilla de celdas iguales
- [x] Snt pidio volver a solo 5 colores (sin variables derivadas extra): `brand` (texto), `bg` (fondo), `surface` (color secundario), `secondary` (color alterno para resaltar), `brand-inverso` (texto alterno). Se eliminaron `--color-secondary-inverso` y `--color-brand-texto` de `index.css` (con eso quedan resueltas las dos notas pendientes de sesiones anteriores sobre esas variables).
- [x] `Button.jsx` reescrito con esos 5 colores nada mas: `primary` = fondo `secondary` + texto `brand-inverso`; `secondary` = fondo `surface` + texto `brand`.
- [x] `pages/Entrenamiento.jsx` rediseñada: camara, nombre de seña, contador y botones pasan a una grilla 2x2 de celdas `aspect-square` del mismo tamaño (verificado: 432×432px cada una, exactas). El contador usa el mismo combo `bg-secondary`/`text-brand-inverso` que el boton primario, tal como pidio Snt de ejemplo.
- [x] Verificado en el navegador en ambos temas (colores exactos via `getComputedStyle`, tamaños via `getBoundingClientRect`). Sin errores de consola.
- [x] A pedido de Snt, estos cambios (sesiones 26, 27 y 28) se dejaron todos en un solo commit (`git reset --soft` + amend manual) en vez de ir generando un commit por cada ronda de ajustes — ninguno de ellos habia sido pusheado todavia.

## Hecho (sesión 29) — correccion: son 2 bloques, no 4
- [x] Snt aclaro: no queria 4 celdas iguales — queria SOLO 2 bloques del mismo tamaño: la camara, y una unica seccion que agrupa nombre de seña + contador + botones juntos. El alto de la camara (432px, heredado de la sesión anterior) estaba bien; lo que pedia era hacerla mas ancha.
- [x] `pages/Entrenamiento.jsx`: vuelto a una grilla de 2 columnas (camara | seccion agrupada), ambas con `h-[27rem]` (432px, el mismo alto de antes) y ancho igualado por el grid (`grid-cols-2`, contenedor `max-w-6xl` en vez de `max-w-4xl`). Adentro de la seccion agrupada, nombre+input, contador y botones se reparten con `justify-between`.
- [x] Verificado con `getBoundingClientRect`: ambos bloques miden exactamente 560×432px (antes eran 432×432 en la version de 4 celdas) — mismo alto, mas ancho, y los dos bloques iguales entre si. Sin errores de consola.
- [x] Snt va a ajustar los colores por su cuenta a partir de aca.

## Hecho (sesión 30) — botones y tipografia del input
- [x] `Button.jsx`: botones mas grandes (`px-8 py-4 text-base`, antes `px-5 py-2.5 text-sm`).
- [x] `pages/Entrenamiento.jsx`: fila de botones centrada (`justify-center`, antes alineados a la izquierda).
- [x] Label "Nombre seña" y el placeholder del input ahora usan `text-brand`/`placeholder:text-brand` (el color de tipografia principal del tema activo), antes heredaban el color por defecto.
- [x] Verificado en el navegador en ambos temas (colores y tamaños exactos por `getComputedStyle`/`getBoundingClientRect`). Sin errores de consola. Se respeto el ajuste de color que Snt esta haciendo por su cuenta en `index.css`.

## Hecho (sesión 31) — pagina de Traduccion implementada
- [x] `Button.jsx` refactorizado: se separaron los estilos de color (`variant`) y de tamaño (`size`, nuevo prop). `size="lg"` es ~10% mas grande que el default (`px-[2.2rem] py-[1.1rem] text-[1.1rem]` vs `px-8 py-4 text-base`) — no afecta a los botones existentes de Entrenamiento, que siguen en `size="default"`.
- [x] `pages/Traduccion.jsx` implementada con la misma base que `Entrenamiento.jsx`: camara a la izquierda (560×432px, igual que antes) y al lado un bloque partido en 2 mitades EXACTAS con CSS Grid (`grid-rows-2`, 204px cada una): arriba el boton "Traducir" (unico boton, `size="lg"`, empieza a la misma altura que la camara), abajo una caja (`bg-surface`/`text-brand`) que mostrara la traduccion que devuelva el backend (por ahora placeholder "La traduccion aparecera aqui"), terminando a la misma altura que el final de la camara.
- [x] Nota tecnica: el primer intento de partir el bloque en 2 mitades iguales fue con `flex flex-col` + `flex-1` + `min-h-0`, pero por alguna razon el navegador no las repartia parejo (180px/228px en vez de 204/204 iguales, con las mismas propiedades flex computadas en ambos). Cambiar a CSS Grid (`grid-rows-2`) resolvio el problema y dio el split exacto esperado.
- [x] Verificado en el navegador en ambos temas: tamaños exactos por `getBoundingClientRect` (camara y bloque de controles ambos 560×432, mitades 204/204), colores correctos por `getComputedStyle`, y confirmado que Entrenamiento sigue exactamente igual (125×56 / 108×56, mismos colores) tras el refactor de `Button.jsx`. Sin errores de consola.
- [x] Con esto quedan resueltos dos pendientes: "usar CameraFeed en Traduccion" y una parte de "definir el contenido de Traduccion" (la estructura visual; falta la logica real).
- [x] A pedido de Snt: el boton "Traducir" y la caja de traduccion quedaron agrupados en un `<section>` (antes un `div`), en vez de sueltos directamente en el grid.
- [x] A esa `<section>` se le agrego el color de las secciones (`bg-surface`, `rounded-2xl`, `p-8` — mismo tratamiento que el panel agrupador de Entrenamiento), para que se vea como un solo bloque agrupado visualmente. Se le saco el `bg-surface` propio a la caja de traduccion (quedaria duplicado/invisible sobre el mismo color del panel). Verificado: 560×432px, misma posicion que la camara, `bg-surface` aplicado correctamente en ambos temas.

## Pendiente / próximos pasos
- [ ] Implementar la logica real de `handleEntrenar`/`handleEnviar` (Entrenamiento) y `handleTraducir` (Traduccion): conectar la captura de muestras y el reconocimiento via `handLandmarker.js` con el backend.
- [ ] Probar `CameraFeed` con acceso real a camara (fuera de la vista previa embebida, que bloquea `getUserMedia`) para confirmar el video en vivo, en ambas paginas.
- [ ] Definir el formato/contrato de la respuesta del backend para pintar la traduccion real en la caja de `Traduccion.jsx` (por ahora es un placeholder de texto).
- [ ] Si más adelante se agregan assets reales de manos/señas, reemplazar los emojis de `IntroSplash.jsx` (`SENAS`) por esos assets.
- [ ] Revisar la intro en pantallas muy angostas (el docking usa `left: 1.5rem` / `sm:2.5rem`, igual que el header real, pero vale la pena confirmarlo en dispositivo).
- [ ] Snt sigue con los "Verificar" pendientes de `.informacion-homepage.md` para afinar el contenido si hace falta (aunque ya está aplicado).
- [ ] Integrar en `App.jsx`: 3 secciones separadas (ya no una sola tarjeta "Que es?"), cada una con su propia burbuja de información mostrando el texto "Detalle".
- [ ] **No hay router** (`react-router-dom` no está instalado). Los enlaces del burger menu ("Inicio" → `/`, "Traductor" → `/traduccion`) son visuales; al no existir rutas reales, no navegan entre `App.jsx` y `Traduccion.jsx` como páginas SPA. Falta decidir e instalar un router para conectarlas de verdad.
- [ ] `Sidebar.jsx` sigue vacío y sin usar — con el burger menu ya implementado, probablemente se pueda eliminar; a confirmar.
- [ ] `Button.jsx` tiene variantes (`primary`, `sidebar`, `burble`, `stop`, `default`) declaradas pero sin estilos ni uso real — unificarlo con la paleta nueva.
- [ ] Extraer estilos repetidos de botones a `Button.jsx` en vez de clases sueltas en `App.jsx`.
- [ ] Contraste de accesibilidad: revisar `secondary` con texto oscuro en fondos claros.
- [ ] `.claude/launch.json` se había borrado del repo; lo recreé solo para poder previsualizar con el navegador embebido — confirmar si se quiere versionado o no.

## Ideas futuras (bajo prioridad)
- [ ] Modo "sistema" explícito (además de claro/oscuro) en el toggle.
- [ ] Animación de transición al cambiar de tema.
