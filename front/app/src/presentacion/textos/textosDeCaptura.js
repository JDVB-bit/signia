/** 💬 Textos que ve el usuario durante la captura de muestras en Entrenamiento. */

import { MOTIVOS_DE_DESCARTE } from '../../dominio/reglasDeGrabacion.js'

/** Motivo de descarte del dominio -> explicacion para el usuario. */
export const TEXTO_POR_MOTIVO_DE_DESCARTE = {
    [MOTIVOS_DE_DESCARTE.DEMASIADO_CORTA]: 'La grabación fue demasiado corta: no se guardó nada.',
    [MOTIVOS_DE_DESCARTE.SIN_MANOS]: 'No se vio ninguna mano: la muestra se descartó.',
}

export const AVISOS_DE_CAPTURA = {
    FALTA_ETIQUETA: 'Escribe el nombre de la seña antes de grabar.',
    PESTANA_OCULTA: 'La grabación se descartó al salir de la pestaña.',
}
