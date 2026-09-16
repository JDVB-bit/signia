/** 🗓️ Identificador de la tanda de grabacion (`sesion` del contrato). */

/** Dispositivo usado cuando no se conoce uno mas concreto. */
export const DISPOSITIVO_POR_DEFECTO = 'local'

const DIGITOS_FECHA = 2
// getMonth() empieza en 0 (enero) y la fecha legible empieza en 1
const DESFASE_MES = 1

/** Fecha + dispositivo: "mismo dia, mismo equipo" aproxima bien una tanda.
 *
 * `sesion` es lo que permite la evaluacion honesta de la Fase 4: el split del
 * dataset es por sesion, nunca aleatorio.
 */
export function idSesion(fecha = new Date(), dispositivo = DISPOSITIVO_POR_DEFECTO) {
    const dia = [
        fecha.getFullYear(),
        String(fecha.getMonth() + DESFASE_MES).padStart(DIGITOS_FECHA, '0'),
        String(fecha.getDate()).padStart(DIGITOS_FECHA, '0'),
    ].join('-')
    return `${dia}-${dispositivo}`
}
