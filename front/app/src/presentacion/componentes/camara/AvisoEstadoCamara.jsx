import { ESTADOS_CAMARA } from '../../estados/estadosDeCamara'

/** Explicacion para cada estado en el que la camara todavia no muestra video. */
const MENSAJE_POR_ESTADO = {
    [ESTADOS_CAMARA.NO_SOPORTADA]: 'Este navegador no permite acceder a la cámara.',
    [ESTADOS_CAMARA.DENEGADA]:
        'Se denegó el acceso a la cámara. Habilítalo en los permisos del navegador para este sitio y vuelve a intentarlo.',
    [ESTADOS_CAMARA.SOLICITANDO]: 'Solicitando acceso a la cámara...',
}

/** Estados desde los que el usuario puede (volver a) pedir la camara. */
const ESTADOS_CON_BOTON = new Set([ESTADOS_CAMARA.INICIAL, ESTADOS_CAMARA.DENEGADA])

/** Contenido que ocupa el recuadro de la camara mientras no esta activa. */
export default function AvisoEstadoCamara({ estado, alActivar }) {
    const mensaje = MENSAJE_POR_ESTADO[estado]

    return (
        <div className="flex flex-col items-center gap-3 p-6 text-center">
            {mensaje && <p className="text-sm opacity-80">{mensaje}</p>}
            {ESTADOS_CON_BOTON.has(estado) && (
                <button
                    type="button"
                    onClick={alActivar}
                    className="rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white transition-opacity hover:opacity-90"
                >
                    Activar cámara
                </button>
            )}
        </div>
    )
}
