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

## Hecho (sesión 32) — aprovechar el ancho en pantallas grandes
- [x] Snt reporto que quedaba mucho espacio vacio en los laterales en pantallas anchas (el grid de camara+seccion estaba topado a `max-w-6xl`=1152px, muy por debajo del ancho maximo de `PageLayout`, 110rem=1760px).
- [x] `pages/Entrenamiento.jsx` y `pages/Traduccion.jsx`: quitado el `max-w-6xl` del grid (ahora `w-full`, sin techo propio — lo unico que lo limita es el `max-w-[110rem]` de `PageLayout`). Alto de los bloques sin cambios (`h-[27rem]`, 432px).
- [x] Verificado con `getBoundingClientRect`: a 1280px de viewport no cambia nada (560px por bloque, coincidia con el viejo tope); a 1920px de viewport ahora cada bloque mide 800px (antes se hubiera quedado en 560, con espacio vacio a los costados) — camara y seccion siguen exactamente iguales entre si en ambas paginas. Sin errores de consola.

## Hecho (sesión 33) — planificación del modelo y del despliegue
- [x] Sesión de diseño (sin tocar código de producto): se analizó la idea de Snt de un endpoint `/entrenar` que llame a un orquestador PyTorch con un método "aprender" incremental.
- [x] Conclusión acordada: la idea es viable en su forma general, con 3 correcciones — (1) separar "capturar muestra" de "entrenar", (2) el entrenamiento es un job por lotes asíncrono, no un paso de gradiente dentro del request HTTP, (3) **el dataset es la fuente de verdad y el modelo es un artefacto derivado** (siempre reconstruible).
- [x] Definido qué va a GitHub: sólo el CÓDIGO del modelo (`model.py`, `train.py`, `preprocess.py`, config) — ni pesos (`.pt`/`.onnx`), ni muestras, ni base de datos. Nada de GitHub Actions para entrenar; Actions queda sólo para lint/tests/deploy.
- [x] Analizadas alternativas de arquitectura del modelo (DTW+kNN como baseline sin entrenamiento, GRU/1D-CNN con softmax reentrenable, y embeddings+prototipos para alta en caliente de señas) y de despliegue (VPS con disco persistente vs PaaS efímero vs HF Spaces; torch para entrenar, onnxruntime para servir).

## Hecho (sesión 34) — modelo de datos y evaluación de Google Cloud
- [x] Confirmado el flujo definitivo con Snt: muestras → almacenamiento → `POST /entrenamientos` reentrena **desde cero con todo el dataset** → nuevo artefacto versionado → puntero "activo" con rollback. El reentrenamiento es a demanda (botón Entrenar), no por cada muestra enviada — coincide con los dos botones que ya existen en `Entrenamiento.jsx`.
- [x] Matiz importante aclarado: las secuencias de landmarks NO van dentro de la DB. Van como ficheros `.npz` en disco/objeto; la DB guarda sólo metadatos (etiqueta, ruta, versión de preprocesado, origen, estado).
- [x] Definido el esquema de tablas: `muestras`, `senas`, `entrenamientos` (jobs) y `modelos` (registro con `activo`).
- [x] Evaluado Google Cloud: viable en dos sabores — (A) Cloud Run + GCS + Firestore + Cloud Run Job para entrenar (serverless, ~0€, más piezas), (B) Compute Engine `e2-micro` del always-free + Docker + SQLite (igual que un VPS, más simple, 1GB de RAM como límite real). Descartados Cloud SQL y Vertex AI por coste/sobredimensión.
- [x] Regla identificada: **SQLite y Cloud Run son incompatibles** (contenedor sin estado + GCS FUSE rompe el locking). Si Cloud Run → Firestore; si VM → SQLite.

## Hecho (sesión 35) — plan de implementación escrito
- [x] Corrección de Snt sobre la semántica de los botones de `Entrenamiento.jsx`: **Entrenar = capturar muestra** (incrementa el contador), **Enviar = llamar al endpoint**. Anotado en el plan; queda abierta la decisión de si "Enviar" dispara además el reentrenamiento.
- [x] Escrito `.claude/plan-implementacion.md` — plan completo en 9 fases (0 a 8) con ficheros a crear, decisiones pendientes y criterio de "hecho" por fase. El despliegue queda explícitamente fuera, con una sección de reglas que garantizan que el software sea independiente de él.
- [x] Mejora del diseño respecto a la sesión anterior: se guardan los landmarks **crudos** (no normalizados) como fuente de verdad, y el preprocesado se aplica al vuelo. Así cambiar la normalización ya NO invalida el dataset — basta reentrenar.
- [x] Definido el vector de features: T=48 frames × 128 (por mano: presencia 1 + posición de muñeca 2 + escala 1 + forma 60). Conserva la posición de la seña en el encuadre, que en LSE es discriminante y se perdería con una normalización ingenua.

## Hecho (sesión 36) — vocabulario abierto y modo continuo
- [x] `T = 48` confirmado por Snt; marcado como decisión cerrada en el plan.
- [x] Retirado el techo de "5 señas" del alcance: el plan pasa a **vocabulario abierto `n`**. `n_clases` se deriva del dataset al entrenar y no se escribe en ninguna parte (ni código, ni front, ni API).
- [x] `model.py` se divide en **`Encoder`** (secuencia → vector) y **`Cabeza`** (vector → decisión), para poder cambiar softmax → prototipos a escala sin tocar encoder, preprocesado ni API.
- [x] Nueva sección **§Escalar a `n` señas** en el plan: tabla de horas de grabación por tamaño de vocabulario (el muro real es el dato, no la arquitectura), y las dos cosas que se rompen a partir de ~100 señas (solo-manos deja de bastar → `PoseLandmarker`; el reentrenamiento completo deja de ser instantáneo).
- [x] Aclaración importante a Snt: "reconocer señas una por una" NO significa que haga una frase seguida y la transcriba. Eso es **segmentación**, un problema aparte — se le dio su propia **Fase 6.5 (modo continuo)** con ventana deslizante + la clase `reposo` como separador + consolidación, y CTC anotado como el límite de ese enfoque.
- [x] Añadido a la Fase 2: si la ambición es vocabulario grande, grabar `PoseLandmarker` desde ya aunque el modelo v1 lo ignore (lo que no se graba hoy no se puede usar mañana sin regrabar).
- [x] Añadidos 3 riesgos nuevos a la tabla del plan (señado fluido en modo continuo, vocabulario sin dato, orden de clases inestable entre artefactos).

## Hecho (sesión 37) — el traductor, no el diccionario
- [x] Snt fijó el propósito del producto: **traducir la frase entera y corrida**. Reconocer una seña por pulsación seria solo un "diccionario inteligente", no un traductor. El plan se reestructuró completo alrededor de eso.
- [x] Confirmado: se graba cuando el usuario **pulsa "Entrenar"** (toggle, sin autodetección) — decision cerrada en el plan.
- [x] El modo continuo deja de ser la "Fase 6.5 opcional" y pasa a ser la **Fase 6, el producto**. El modo aislado se reencuadra como el *camino de entrenamiento* (captura de dato etiquetado), no como una forma alternativa de usar la app.
- [x] Tres consecuencias arrastradas hacia atras, que son el valor real de esta sesion:
  1. **La inferencia se muda al navegador** (`onnxruntime-web`): el modo continuo predice ~6 veces/segundo y una peticion HTTP por ventana es insostenible. El backend sale del camino critico de la traduccion y pasa a servir el artefacto (`GET /modelos/activo/weights.onnx`). Un backend caido ya no rompe la demo.
  2. **Hay que grabar frases completas** (Fase 2c, nueva) etiquetadas con la secuencia de palabras: para medir WER, para calibrar los umbrales de consolidacion, y porque es el dato que necesita el CTC de la v2. Barato hoy, caro despues.
  3. **La metrica pasa a ser WER** (Word Error Rate) por frase, no accuracy por muestra. Un modelo con 95% aislado puede transcribir basura. Se desglosa en inserciones / borrados / sustituciones porque cada error se arregla distinto.
- [x] Resuelta la tension que creaba inferir en JS: el preprocesado seguia teniendo que existir una sola vez. Solucion — la **normalizacion va dentro del grafo ONNX** (mismo codigo en Python y en el navegador) y solo el remuestreo temporal (aritmetica de indices) se escribe dos veces, con un **test de conformidad** contra fixtures generadas por Python.
- [x] `reposo` promovida a pieza critica: en modo continuo **es el segmentador**. Necesita 2-3× mas muestras que una seña normal e incluir frames de transicion entre señas.
- [x] Añadido el **roadmap v2 (CTC)** como seccion propia: la ventana deslizante es un heuristico que exige micro-pausas; el señado fluido pide entrenar sobre frases con perdida CTC. Nada de las fases 0-5 se tira.
- [x] `umbrales.json` añadido al artefacto del modelo (confianza minima y `k` de consolidacion), calibrados con las frases de la Fase 2c en vez de puestos a ojo.

## Hecho (sesión 38) — arquitectura en dos etapas (glosas → texto)
- [x] Snt corrigió una ambigüedad del plan: **el modelo NO se entrena con frases**, se entrena con señas. Entrenar con frases como unidad seria inviable — "no podemos predecir como hablara alguien". Las frases de la Fase 2c eran ya solo para evaluar/calibrar, pero el plan daba pie a la lectura contraria: se reescribió con un aviso explícito y el por qué de la generalización (unidad = seña → cualquier combinación y orden).
- [x] Recuperada del planteamiento original de Snt la **arquitectura en dos etapas**, que faltaba en el plan:
  - **Etapa 1 (nuestro modelo, PyTorch/ONNX):** señas → secuencia de **glosas** (palabras sueltas, sin conjugar, en orden LSE). Corre en el navegador.
  - **Etapa 2 (agente de texto / LLM):** glosas → español natural. Es un problema de TEXTO, no de visión. Nueva **Fase 6b**.
- [x] Añadida la sección "Arquitectura en dos etapas" al principio del plan, con el diagrama del pipeline y el principio nuevo (·6: el modelo aprende señas, nunca frases).
- [x] Fase 6 renombrada a "Reconocimiento continuo → secuencia de glosas (etapa 1)" para que no se confunda con el producto final.
- [x] **Fase 6b diseñada:** `POST /redactar` en el backend (la clave del LLM no puede estar en el navegador), **una llamada por frase**, no por ventana. Se dispara al cerrar la frase (stop manual o `reposo` >~2s), no palabra a palabra. Fallback a mostrar glosas crudas si no hay backend/LLM.
- [x] Tres guardas en `/redactar`: validar cada glosa contra la tabla `senas` **antes** de construir el prompt (cierra la inyección de prompt: vocabulario cerrado = superficie cerrada), instrucción anti-invención + temperatura baja, y la tira de glosas siempre visible junto al texto como evidencia.
- [x] **Dos métricas separadas:** WER sobre glosas mide nuestro modelo; la calidad del español se juzga aparte pasando las glosas de REFERENCIA por la etapa 2 (aisla el fallo de cada etapa). `evaluar_frases.py` es también el que calibra `k` y el umbral y los escribe en `umbrales.json`.
- [x] Aclarado en el roadmap v2 que **CTC tampoco memoriza frases**: su alfabeto de salida es el vocabulario de señas y de una frase aprende la *alineación*, no la frase como unidad — sigue generalizando a órdenes nunca vistos. Se explicita para que no parezca que contradice el principio 6.
- [x] Añadidos 4 riesgos nuevos (confundir etapas al diagnosticar, el LLM inventando contenido no señado, inyección vía glosas, dependencia del servicio externo).
- [x] Anotado que `LLM_API_KEY` es el único secreto real del proyecto: sólo en el backend, por variable de entorno, nunca versionada.

## Hecho (sesión 39) — Fase 0 implementada y testeada

- [x] **Paquete `model/signia_modelo/` con Clean Architecture en tres capas**, con la única regla de que las de dentro no importan nada de las de fuera:
  - `dominio/` (python puro, sin numpy ni torch): `contrato.py` (T=48, F=128, índices de muñeca/nudillo, EPS), `entidades.py` (`Lado`, `Mano`, `Frame`, `Muestra` → `MuestraAislada` / `MuestraFrase`), `errores.py` y `puertos.py` (`Protocol`: `Remuestreador`, `LectorMuestras`, `EscritorMuestras`, `RepositorioMuestras`).
  - `aplicacion/` (numpy): `remuestreo.py` y `preprocess.py` (muestra cruda → `(48,2,21,3)` + presencia `(48,2)`).
  - `infra/`: `json_contrato.py` (validación de la frontera), `repo_ficheros.py` (dataset en disco, `DATOS_DIR` por entorno), `normalizacion_torch.py` (las features, dentro del grafo) y `exportacion_onnx.py`.
- [x] **Entidades inmutables que se validan a sí mismas**: si existe la instancia, cumple el contrato. Las capas de arriba no repiten validaciones.
- [x] **Regla única para dos manos con el mismo `lado`** (falso positivo de MediaPipe): gana la de mayor `score`. Vive sólo en `Frame.mano()`.
- [x] **Remuestreo por selección de índices, no interpolación** (interpolar entre un frame con mano y otro sin ella inventaría medias manos). Redondeo escrito como `int(x+0.5)` a propósito: `round()` de Python redondea al par y `Math.round` de JS no — esa diferencia sola bastaría para que el navegador y el entrenamiento vieran tensores distintos. Hay un test dedicado a ese caso.
- [x] **Normalización dentro del grafo ONNX** (`Normalizacion`, sin parámetros): presencia(1) + posición de muñeca(2) + escala(1) + forma(60) por mano → 128. La mano ausente sale en ceros exactos y la escala se clampa, así que el grafo no puede producir `NaN`.
- [x] **Exportación con el exportador nuevo (`dynamo=True`) y ejes dinámicos compartidos** (lote y tiempo), más test de paridad torch ↔ onnxruntime a 1e-5 con 0, 1 y 2 manos y con 1/12/48/120 frames.
- [x] **`model/contrato.md`**: el contrato en prosa, fuente de verdad, con la tabla de qué cambio rompe qué.
- [x] **Fixtures de conformidad** (`model/tests/fixtures/*.json`, 6 casos límite) + `scripts/generar_fixtures.py`. Falta el lado JS, que los leerá tal cual.
- [x] **164 tests con pytest, todos en verde** (`pytest -m "not torch"` deja 138 que corren sin torch en ~3 s). Cubren: validación de entidades, remuestreo y sus bordes, ranuras/presencia del tensor, inyección del remuestreador (DIP), round-trip JSON, saneado de rutas (la etiqueta viene del usuario y acaba siendo carpeta), invariancias de la normalización y paridad ONNX.
- [x] `model/pyproject.toml` (paquete instalable + config de pytest con marcadores `torch`/`onnx`), `model/README.md`, `model/.gitignore` (`data/`, `artefactos/`, `__pycache__/`) y `requirements.txt` con `onnx`/`onnxscript`/`onnxruntime`/`pytest` fijados.

## Hecho (sesión 40) — Fase 1: captura de muestras en el front

- [x] **`src/lib/preprocess.js`** — el gemelo en JS del preprocesado de Python: los mismos 48 índices, la misma regla para dos manos del mismo lado y el mismo redondeo (`Math.round` == `int(x+0.5)`). Devuelve arrays planos, que es lo que espera `ort.Tensor` en la Fase 6.
- [x] **Test de conformidad JS ↔ Python** (`src/lib/__tests__/conformidad.test.js`): lee los MISMOS fixtures que verifica pytest y compara índices, presencia y landmarks a 1e-5. Comprobado que la red tiene dientes: cambiar `Math.round` por `Math.floor` tumba 8 tests. **Esto cierra la Fase 0.**
- [x] **`src/lib/muestras.js`** — toda la lógica que se puede probar sin cámara: `frameDesdeResultado` (MediaPipe → frame del contrato), `crearMuestra`, `motivoDeDescarte`, `debeCerrarPorTiempo`, `nombreDeFichero`. El hook solo orquesta.
- [x] **`src/lib/dibujarMano.js`** — overlay del esqueleto sobre el vídeo, con las 21 conexiones, un color por mano y **el rótulo del lado junto a la muñeca**. Ese rótulo es la verificación empírica del handedness que pedía el plan, convertida en una comprobación de 10 segundos.
- [x] **`src/lib/useCapturaSenas.js`** — el bucle: `requestAnimationFrame` → `detectForVideo` → buffer → muestra. API `{ grabando, alternarGrabacion, muestras, borrarUltima, exportar }` + estado, segundos y avisos. Tope de 4 s por grabación.
- [x] **Se descarta la grabación si la pestaña se oculta.** Descubierto probando: el navegador congela `requestAnimationFrame` en una pestaña oculta, y al volver el contador ya había pasado el tope y cerraba una muestra con cuatro frames sueltos. Además, una seña que no se estaba mirando no es dato bueno.
- [x] **`CameraFeed`** acepta ahora una `ref` externa al `<video>`, una capa de overlay (`children`) y `resaltado` para el borde mientras graba, sin romper su uso anterior en `Traduccion`.
- [x] **`Entrenamiento.jsx` conectado de verdad:** "Entrenar" graba una muestra (pulsar/pulsar), el contador sube, "Enviar" descarga el JSON del lote, "Borrar ultima muestra" deshace. Indicadores de manos detectadas, segundos grabando y sesión.
- [x] `Button.jsx` acepta `disabled` (y `type="button"`), para que Entrenar/Enviar se apaguen cuando no hay cámara o no hay muestras.
- [x] **93 tests de vitest en verde** + los 164 de pytest. Verificado además en el navegador con una cámara falsa (un canvas con una foto de manos reales): MediaPipe detecta, el esqueleto se dibuja alineado con el vídeo espejado, el contador sube y el JSON exportado **pasa el validador del contrato en Python y llega hasta las features `(1, 48, 128)` sin NaN**.

## Hecho (sesión 41) — auditoría y cumplimiento de `.claude/claude.md` y `rules.md`

Rama `refactor/cumplimiento-reglas`, 12 commits atómicos (Conventional Commits, cada uno compila y pasa tests).

- [x] **Infra del repo:** `.gitignore` con entornos de Python y artefactos (`*.onnx`, `*.pt`, `*.npz`, `*.sqlite`, `back/data/`); Docker con Node 24 LTS (Node 20 ya sin soporte), pnpm fijado en `packageManager`, sin el `|| npm ci` que ocultaba fallos; nginx cachea `/assets/`; `index.html` con `lang="es"`, título y el `favicon.svg` que faltaba (daba 404).
- [x] **Modelo (Python), un archivo por responsabilidad:** `dominio/entidades/` (una entidad por archivo) y `dominio/puertos/` (un puerto por archivo) con reexport en `__init__`; en `infra/` se separan `json_contrato` (dict↔entidad) de `ficheros_json` (disco), `nombres_de_ruta`, `configuracion_datos`, `exportacion_onnx` y `ejecucion_onnx`. Constantes con nombre (`SCORE_MINIMO/MAXIMO`, `OPSET_ONNX`, ejes, carpetas). 164 tests en verde.
- [x] **Front en Clean Architecture:** `lib/` y `utils/` desaparecen. Ahora `src/dominio`, `src/aplicacion`, `src/infra/{mediapipe,canvas,navegador}` y `src/presentacion/{paginas,componentes,hooks,estados,textos,estilos}`, con `rutas.js` como única fuente de URLs.
- [x] **`useCapturaSenas` (236 líneas, 6 responsabilidades) partido** en `useDetectorDeManos`, `useBucleDeDeteccion`, `useGrabacionDeMuestra` y `useMuestrasCapturadas`. El dominio devuelve códigos de descarte y la presentación pone el texto.
- [x] **Bugs/riesgos corregidos de paso:** (1) el detector de MediaPipe cae a CPU si la GPU falla y no cachea una promesa rechazada; (2) `localStorage`/`sessionStorage` envueltos en `almacenamientoSeguro` (en modo privado lanzaban y rompían la app); (3) `useCamara` descarta respuestas tardías de `getUserMedia` — el doble montaje de StrictMode dejaba un flujo de cámara encendido; (4) apagar la cámara a mitad de grabación la aborta.
- [x] **Código muerto eliminado:** `Sidebar.jsx`, variantes vacías de `Button` (`sidebar`, `burble`, `stop`, `default`), `setTraduccion` sin uso. Lint de oxlint limpio.
- [x] **Duplicaciones eliminadas:** lógica de Escape (BurgerMenu/InfoBubble → `useCerrarConEscape`), `h2` de título copiado por página (`TituloPagina`/`TituloAnimado`), duraciones de la intro escritas en JS y en CSS (ahora variables CSS desde una única fuente), rutas en router y menú.
- [x] **Entrenamiento:** indicadores y contador extraídos a `componentes/captura/`; los cuatro ternarios anidados del mensaje de estado → `mensajeDeEstadoDeCaptura` con test.
- [x] **Traducción honesta:** el botón "Traducir" no hacía nada; ahora está deshabilitado y explica que se activará con el modelo entrenado.
- [x] **UX/accesibilidad:** tildes en todos los textos visibles, lema del header como `<p>` (rompía la jerarquía de encabezados), `aria-live` en mensajes de estado, `prefers-reduced-motion` en las animaciones globales.
- [x] **Rule 2 — README en cada directorio** (51 en total) con archivos, capa a la que pertenecen y ejemplos. README raíz nuevo.
- [x] Comentarios multilínea dentro de funciones condensados a una línea (se mantienen los docstrings de módulo/clase/función).
- [x] Front: 105 tests de Vitest (antes 93) + build OK; verificado en el navegador (Inicio, Entrenamiento con cámara denegada, Traducción, menú + Escape, cambio de tema) sin errores de consola.
- [x] **Captura verificada por Snt con cámara real** tras la refactorización: vídeo, detección, esqueleto, grabación, contador y descarga del JSON funcionan (el navegador embebido bloquea la cámara, por eso lo confirmó Snt).
- [x] Snt considera no prioritarios en esta sesión: revisar la compilación commit a commit, construir la imagen Docker, ver la intro en limpio y auditar versiones de dependencias (quedan abajo como técnica de baja prioridad).
- [x] ⚠️ Cambio de contenido a revisar por Snt: "Lengua de Señas Espanola" → **"Lengua de Signos Española"** (nombre oficial de la LSE) y "lenguaje de señas" → "lengua de señas" en el título.

## Pendiente / próximos pasos

### 🔴 Decisiones de Snt (bloquean fases)
- [ ] **Verificar el handedness con el vídeo espejado** antes de grabar: levantar la mano derecha y leer el rótulo; si dice "izquierda", `INVERTIR_LADO = true` en `front/app/src/infra/mediapipe/ladoDesdeCategoria.js`.
- [ ] Decidir el vocabulario inicial (recomendado 5-10 señas + `reposo`) para arrancar la Fase 2.
- [ ] Decidir si se graba `PoseLandmarker` desde el principio — única decisión irreversible de la Fase 2.
- [ ] Decidir si "Enviar" dispara el reentrenamiento (opción A del plan) o queda como acción de administración (opción B).
- [ ] Elegir proveedor/modelo LLM de la etapa 2 y escribir el prompt (`back/app/dominio/prompt.py`).
- [ ] Destino de despliegue (Cloud Run+GCS+Firestore vs `e2-micro`+SQLite vs VPS).

### 🟠 Producto
- [ ] **El contenido de Inicio promete cosas que el producto aún no hace** ("traduce en tiempo real", "frases de hasta 5 palabras"). Además "hasta 5 palabras" contradice el plan actual (vocabulario abierto de `n` señas). Reescribir con Snt para que refleje el estado real.
- [ ] Mover "Entrenamiento" fuera del menú público (o protegerlo): es una herramienta interna de captura, no algo para el usuario final.
- [ ] Guardar el lote de muestras en IndexedDB mientras no exista `POST /muestras`: hoy recargar la página pierde todas las muestras no descargadas.
- [ ] Confirmación antes de "Borrar última muestra" o botón de deshacer.

### 🟡 Técnica
- [ ] **Test de contrato cruzado JS ↔ Python — al empezar la Fase 2** (acordado con Snt). Hoy la conformidad solo detecta divergencias que cambian el **tensor**: si alguien toca `SCHEMA`, `IDX_MUNECA` o `N_MANOS` en un solo lado, nadie se entera hasta mucho después. Un test que lea `model/signia_modelo/dominio/contrato.py` como texto (o un JSON generado por `scripts/`) y lo compare con `front/app/src/dominio/contrato.js` cierra ese hueco. Hacerlo **antes** de grabar el dataset: después, una divergencia ya habría contaminado muestras.
- [ ] (Baja) Construir y probar la imagen Docker del front (Node 24 + pnpm 11 + nginx nuevo).
- [ ] (Baja) Auditar versiones de dependencias del front y del modelo (regla 1).
- [ ] (Baja) Ver la intro en una ventana limpia tras pasar sus duraciones a variables CSS.
- [ ] Fase 2 del plan: `model/scripts/inspeccionar.py` y grabación del dataset.
- [ ] Fase 5: backend (`POST /muestras`, `GET /modelos/activo`) con la estructura por capas descrita en `back/README.md`.
- [ ] Tests de componentes/hooks de React (`@testing-library/react` + `jsdom`): hoy solo se prueba lógica pura.
- [ ] CI con GitHub Actions: `pnpm lint && pnpm test && pnpm build` y `pytest -m "not torch"` en cada PR.
- [ ] `senas-persona3.jpg` pesa 940 KB: convertir a WebP/AVIF.
- [ ] Contraste de accesibilidad: revisar `secondary` con texto oscuro en fondos claros y el `placeholder` en `brand`.
- [ ] Unificar idioma de los nombres de componentes (hoy conviven `CameraFeed`/`Button` con `ContadorDeMuestras`).
- [ ] Revisar la intro en pantallas muy angostas (docking con `left: 1.5rem`).
- [ ] Si llegan assets reales de manos/señas, reemplazar los emojis de `IntroSplash`.
- [ ] Nunca promover un modelo con métricas peores que el activo y escribir el artefacto de forma atómica (temporal + `rename`) — Fase 7.
- [ ] Proteger `/muestras` y `/entrenamientos` con token — Fase 8.

## Ideas futuras (bajo prioridad)
- [ ] Modo "sistema" explícito (además de claro/oscuro) en el toggle.
- [ ] Animación de transición al cambiar de tema.
