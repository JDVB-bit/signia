/** Tarjeta de seccion con titulo, usada para los bloques de contenido de Inicio. */
export default function SectionCard({ title, className = '', children }) {
    return (
        <section className={`rounded-lg bg-surface p-8 lg:p-10 ${className}`}>
            <h3 className="text-lg font-semibold text-brand">{title}</h3>
            {children}
        </section>
    )
}
