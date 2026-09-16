/** Numero grande con las muestras tomadas en esta sesion de entrenamiento. */
export default function ContadorDeMuestras({ cantidad }) {
    return (
        <div className="flex flex-col items-center gap-1 rounded-2xl bg-secondary p-6 text-brand-inverso shadow-md">
            <span className="text-5xl font-extrabold leading-none">{cantidad}</span>
            <span className="text-xs font-medium uppercase tracking-wide opacity-90">Muestras tomadas</span>
        </div>
    )
}
