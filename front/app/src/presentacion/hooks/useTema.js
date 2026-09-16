/** 🌗 Estado del tema claro/oscuro, sincronizado con el documento y la preferencia guardada. */

import { useCallback, useEffect, useState } from 'react'

import {
    aplicarTemaOscuro,
    guardarTemaOscuro,
    temaOscuroPreferido,
} from '../../infra/navegador/preferenciaDeTema.js'

export default function useTema() {
    const [oscuro, setOscuro] = useState(temaOscuroPreferido)

    useEffect(() => {
        aplicarTemaOscuro(oscuro)
        guardarTemaOscuro(oscuro)
    }, [oscuro])

    const alternarTema = useCallback(() => setOscuro((previo) => !previo), [])

    return { oscuro, alternarTema }
}
