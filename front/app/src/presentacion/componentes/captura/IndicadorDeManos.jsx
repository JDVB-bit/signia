/** Etiqueta sobre el video con cuantas manos esta viendo el detector ahora mismo. */
export default function IndicadorDeManos({ cantidad }) {
    const texto = cantidad === 0 ? 'sin manos' : `${cantidad} mano${cantidad > 1 ? 's' : ''}`

    return <span className="rounded-full bg-brand-inverso/70 px-3 py-1 text-bg">{texto}</span>
}
