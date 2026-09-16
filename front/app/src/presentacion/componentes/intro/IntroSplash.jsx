import { useEffect, useRef, useState } from 'react'
import './IntroSplash.css'

// Duraciones de cada fase (ms). El total se queda comodo por debajo del
// limite de 6s que se pidio para toda la animacion.
const DURACION_APARICION_MS = 850
const DURACION_ESPERA_MS = 400
const DURACION_SUCCION_MS = 2800
const DURACION_CROSSFADE_MS = 350
const RETRASO_INICIAL_MS = 250

const T_APARICION_FIN = RETRASO_INICIAL_MS + DURACION_APARICION_MS
const T_ESPERA_FIN = T_APARICION_FIN + DURACION_ESPERA_MS
const T_SUCCION_FIN = T_ESPERA_FIN + DURACION_SUCCION_MS
const T_CROSSFADE_FIN = T_SUCCION_FIN + DURACION_CROSSFADE_MS
const DURACION_TOTAL_MS = T_CROSSFADE_FIN // ~4.65s

// Sin assets de manos todavia: se simulan las "senas" con emojis que van
// cambiando en la barra de carga, tal como se pidio como alternativa.
const SENAS = [
    { desde: 0, icono: '🖐️' },
    { desde: 25, icono: '🤟' },
    { desde: 75, icono: '🤙' },
    { desde: 99, icono: '👌' },
]

function senaActual(progreso) {
    let icono = SENAS[0].icono
    for (const paso of SENAS) {
        if (progreso >= paso.desde) icono = paso.icono
    }
    return icono
}

/** Pantalla de carga inicial. Se muestra una unica vez (la primera vez que
 * alguien entra al sitio); recargar la pagina no la vuelve a disparar,
 * eso lo decide quien use este componente guardando el resultado de
 * onFinish. Mientras esta activa, no debe montarse ninguna otra parte de
 * la app (ni sus animaciones). */
export default function IntroSplash({ onFinish }) {
    const [progreso, setProgreso] = useState(0)
    const [fase, setFase] = useState('aparicion')
    const inicioRef = useRef(null)
    const frameRef = useRef(null)
    const onFinishRef = useRef(onFinish)
    onFinishRef.current = onFinish

    useEffect(() => {
        inicioRef.current = performance.now()

        const tick = (ahora) => {
            const transcurrido = ahora - inicioRef.current
            setProgreso(Math.min(100, (transcurrido / DURACION_TOTAL_MS) * 100))

            if (transcurrido < T_APARICION_FIN) {
                setFase('aparicion')
            } else if (transcurrido < T_ESPERA_FIN) {
                setFase('espera')
            } else if (transcurrido < T_SUCCION_FIN) {
                setFase('succion')
            } else if (transcurrido < T_CROSSFADE_FIN) {
                setFase('crossfade')
            } else {
                onFinishRef.current?.()
                return
            }

            frameRef.current = requestAnimationFrame(tick)
        }

        frameRef.current = requestAnimationFrame(tick)
        return () => cancelAnimationFrame(frameRef.current)
    }, [])

    return (
        <div className={`intro-overlay intro-overlay--${fase}`} role="presentation" aria-hidden="true">
            <div className={`intro-marca intro-marca--${fase}`}>
                <span className="intro-titulo">SignIA</span>
                <span className="intro-lema">Manos que hablan. Tecnologia que escucha</span>
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
