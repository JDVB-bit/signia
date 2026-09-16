/** 📷 Ciclo de vida de la camara: pedir permiso, conectar el flujo al <video> y apagarla. */

import { useCallback, useEffect, useRef, useState } from 'react'

import { abrirCamara, camaraSoportada, cerrarCamara } from '../../infra/navegador/camara.js'
import {
    permisoConcedidoEnEstaVisita,
    recordarPermisoDeCamara,
} from '../../infra/navegador/permisoDeCamara.js'

export const ESTADOS_CAMARA = Object.freeze({
    INICIAL: 'inicial',
    SOLICITANDO: 'solicitando',
    ACTIVA: 'activa',
    DENEGADA: 'denegada',
    NO_SOPORTADA: 'no-soportada',
})

/** Gestiona la camara que se muestra en `videoRef`.
 *
 * Si en esta visita ya se concedio el permiso, se activa sola al montar; al
 * desmontar siempre se apaga, para que la luz de la camara no quede encendida.
 */
export default function useCamara(videoRef) {
    const [estado, setEstado] = useState(ESTADOS_CAMARA.INICIAL)
    const flujoRef = useRef(null)
    // Cambia en cada montaje/desmontaje: una respuesta de otra "generacion" llega tarde y se descarta
    const generacionRef = useRef(0)

    const activar = useCallback(async () => {
        if (!camaraSoportada()) {
            setEstado(ESTADOS_CAMARA.NO_SOPORTADA)
            return
        }

        const generacion = generacionRef.current
        setEstado(ESTADOS_CAMARA.SOLICITANDO)
        try {
            const flujo = await abrirCamara()
            if (generacion !== generacionRef.current) {
                cerrarCamara(flujo)
                return
            }
            // Una segunda activacion reemplaza el flujo anterior en vez de dejarlo encendido
            cerrarCamara(flujoRef.current)
            flujoRef.current = flujo
            if (videoRef.current) videoRef.current.srcObject = flujo
            setEstado(ESTADOS_CAMARA.ACTIVA)
            recordarPermisoDeCamara(true)
        } catch {
            recordarPermisoDeCamara(false)
            if (generacion === generacionRef.current) setEstado(ESTADOS_CAMARA.DENEGADA)
        }
    }, [videoRef])

    useEffect(() => {
        generacionRef.current += 1
        if (permisoConcedidoEnEstaVisita()) activar()

        return () => {
            generacionRef.current += 1
            cerrarCamara(flujoRef.current)
            flujoRef.current = null
        }
    }, [activar])

    return { estado, activar }
}
