/** Mano de un lado dentro de un frame, o null si no la hay.
 *
 * MediaPipe puede reportar dos manos con el mismo lado (falso positivo). La
 * regla, identica a `Frame.mano()` en Python: gana la de mayor score; a
 * igualdad, la primera.
 */
export function manoDelFrame(frame, lado) {
    let elegida = null
    for (const mano of frame.manos ?? []) {
        if (mano.lado !== lado) continue
        // Solo un score ESTRICTAMENTE mayor desplaza: asi el empate favorece a la primera
        if (elegida === null || mano.score > elegida.score) elegida = mano
    }
    return elegida
}
