/** Decimales del cronometro: suficientes para ver que avanza, sin parpadeo de cifras. */
const DECIMALES_SEGUNDOS = 1

/** Punto rojo pulsante + segundos transcurridos mientras se graba una muestra. */
export default function IndicadorDeGrabacion({ segundos }) {
    return (
        <span className="flex items-center gap-2 rounded-full bg-secondary px-3 py-1 text-brand-inverso">
            <span className="h-2 w-2 animate-pulse rounded-full bg-red-500" />
            grabando {segundos.toFixed(DECIMALES_SEGUNDOS)}s
        </span>
    )
}
