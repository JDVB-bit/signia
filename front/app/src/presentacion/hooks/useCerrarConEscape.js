/** ⎋ Cierra un panel (menu, dialogo) al pulsar Escape mientras esta abierto. */

import { useEffect } from 'react'

const TECLA_ESCAPE = 'Escape'

export default function useCerrarConEscape(abierto, cerrar) {
    useEffect(() => {
        if (!abierto) return undefined

        const alPulsarTecla = (evento) => {
            if (evento.key === TECLA_ESCAPE) cerrar()
        }
        document.addEventListener('keydown', alPulsarTecla)
        return () => document.removeEventListener('keydown', alPulsarTecla)
    }, [abierto, cerrar])
}
