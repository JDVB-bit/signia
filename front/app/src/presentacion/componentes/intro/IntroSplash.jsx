import { useEffect, useRef, useState } from 'react'

import './IntroSplash.css'

// ⏱️ Duraciones de cada fase: unica fuente, el CSS las recibe como variables
const RETRASO_INICIAL_MS = 250
const DURACION_APARICION_MS = 850
const DURACION_ESPERA_MS = 400
const DURACION_SUCCION_MS = 2800
const DURACION_CROSSFADE_MS = 350

// Instantes (desde el inicio) en que termina cada fase
const FIN_APARICION_MS = RETRASO_INICIAL_MS + DURACION_APARICION_MS
const FIN_ESPERA_MS = FIN_APARICION_MS + DURACION_ESPERA_MS
const FIN_SUCCION_MS = FIN_ESPERA_MS + DURACION_SUCCION_MS
const DURACION_TOTAL_MS = FIN_SUCCION_MS + DURACION_CROSSFADE_MS

const PROGRESO_COMPLETO = 100

const FASES = Object.freeze({
    APARICION: 'aparicion',
    ESPERA: 'espera',
    SUCCION: 'succion',
    CROSSFADE: 'crossfade',
})

/** Variables CSS con las duraciones, para que las animaciones no repitan los numeros. */
const VARIABLES_DE_DURACION = {
    '--intro-duracion-aparicion': `${DURACION_APARICION_MS}ms`,
    '--intro-duracion-succion': `${DURACION_SUCCION_MS}ms`,
    '--intro-duracion-crossfade': `${DURACION_CROSSFADE_MS}ms`,
}

// Sin assets de manos todavia: emojis que cambian segun el % de la barra de carga
const SENAS_POR_PROGRESO = [
    { desde: 0, icono: '🖐️' },
    { desde: 25, icono: '🤟' },
    { desde: 75, icono: '🤙' },
    { desde: 99, icono: '👌' },
]

/** Emoji que corresponde al progreso actual (el ultimo umbral superado). */
function senaActual(progreso) {
    let icono = SENAS_POR_PROGRESO[0].icono
    for (const paso of SENAS_POR_PROGRESO) {
        if (progreso >= paso.desde) icono = paso.icono
    }
    return icono
}

/** Fase de la animacion en la que se esta tras `transcurridoMs`, o null si ya termino. */
function faseEn(transcurridoMs) {
    if (transcurridoMs < FIN_APARICION_MS) return FASES.APARICION
    if (transcurridoMs < FIN_ESPERA_MS) return FASES.ESPERA
    if (transcurridoMs < FIN_SUCCION_MS) return FASES.SUCCION
    if (transcurridoMs < DURACION_TOTAL_MS) return FASES.CROSSFADE
    return null
}

/** Pantalla de carga inicial: la marca aparece, se "succiona" hacia el header y da paso al sitio.
 *
 * Quien la usa decide cuando mostrarla y guarda que ya se vio en `onFinish`.
 */
export default function IntroSplash({ onFinish }) {
    const [progreso, setProgreso] = useState(0)
    const [fase, setFase] = useState(FASES.APARICION)
    const onFinishRef = useRef(onFinish)

    useEffect(() => {
        onFinishRef.current = onFinish
    }, [onFinish])

    useEffect(() => {
        const inicio = performance.now()
        let frame = 0

        const tick = (ahora) => {
            const transcurrido = ahora - inicio
            setProgreso(Math.min(PROGRESO_COMPLETO, (transcurrido / DURACION_TOTAL_MS) * PROGRESO_COMPLETO))

            const faseActual = faseEn(transcurrido)
            if (faseActual === null) {
                onFinishRef.current?.()
                return
            }
            setFase(faseActual)
            frame = requestAnimationFrame(tick)
        }

        frame = requestAnimationFrame(tick)
        return () => cancelAnimationFrame(frame)
    }, [])

    return (
        <div
            className={`intro-overlay intro-overlay--${fase}`}
            style={VARIABLES_DE_DURACION}
            role="presentation"
            aria-hidden="true"
        >
            <div className={`intro-marca intro-marca--${fase}`}>
                <span className="intro-titulo">SignIA</span>
                <span className="intro-lema">Manos que hablan. Tecnología que escucha</span>
            </div>

            <div className={`intro-carga intro-carga--${fase}`}>
                <div className="intro-barra">
                    <div className="intro-barra__relleno" style={{ width: `${progreso}%` }} />
                    <span className="intro-mano" style={{ left: `${progreso}%` }}>
                        {senaActual(progreso)}
                    </span>
                </div>
            </div>
        </div>
    )
}
