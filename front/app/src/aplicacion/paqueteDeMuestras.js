/** 📦 Lote de muestras listo para exportar (hoy un fichero, en la Fase 5 `POST /muestras`). */

import { SCHEMA } from '../dominio/contrato.js'
import { idSesion } from './sesionDeGrabacion.js'

const PREFIJO_FICHERO = 'signia'
const EXTENSION_FICHERO = '.json'

/** Envuelve las muestras con su schema: exactamente lo que consumira el endpoint. */
export function paqueteDeMuestras(muestras) {
    return { schema: SCHEMA, muestras }
}

/** Nombre legible y ordenable del fichero exportado. */
export function nombreDeFichero(muestras, fecha = new Date()) {
    const etiquetas = [...new Set(muestras.map((muestra) => muestra.etiqueta))]
    // Un lote de una sola seña se nombra por ella; uno mixto, por cuantas trae
    const descripcion = etiquetas.length === 1 ? etiquetas[0] : `${etiquetas.length}-senas`
    return `${PREFIJO_FICHERO}-${descripcion}-${idSesion(fecha)}${EXTENSION_FICHERO}`
}
