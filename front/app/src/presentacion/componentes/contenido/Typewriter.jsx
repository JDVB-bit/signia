import { useEffect, useState } from 'react'

/** Tiempo entre caracteres: rapido para no hacer esperar, lento para que se perciba la escritura. */
const MS_POR_CARACTER = 25
const CURSOR = '▌'

/** Animacion de escritura: revela el texto caracter a caracter con un cursor parpadeante. */
export default function Typewriter({ text, speed = MS_POR_CARACTER, className = '' }) {
    const [visible, setVisible] = useState('')
    const terminado = visible.length >= text.length

    useEffect(() => {
        setVisible('')
        let caracteres = 0
        const intervalo = setInterval(() => {
            caracteres += 1
            setVisible(text.slice(0, caracteres))
            if (caracteres >= text.length) clearInterval(intervalo)
        }, speed)
        return () => clearInterval(intervalo)
    }, [text, speed])

    return (
        <p className={className}>
            {visible}
            {!terminado && <span className="animate-pulse">{CURSOR}</span>}
        </p>
    )
}
